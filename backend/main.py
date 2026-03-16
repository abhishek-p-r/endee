"""FastAPI backend for Endee AI Knowledge Assistant."""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import PyPDF2
import io

from backend.config import settings
from backend.rag_pipeline import get_rag_pipeline
from backend.endee_client import get_endee_client
from backend.logging_config import get_logger
from backend.analytics import get_analytics
from backend.cache_manager import get_query_cache
from backend.query_optimizer import get_query_optimizer

logger = get_logger("main")

# Initialize FastAPI app
app = FastAPI(
    title="Endee AI Knowledge Assistant",
    description="Multi-Agent RAG System powered by Endee Vector Database",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str
    session_id: str = "default"
    use_conversation_history: bool = True


class DocumentRequest(BaseModel):
    """Request model for ingesting documents."""
    documents: List[dict]
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str
    version: str
    endee_connected: bool


# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        endee_client = await get_endee_client()
        endee_connected = await endee_client.health_check()
        
        return HealthResponse(
            status="healthy",
            service="Endee AI Knowledge Assistant",
            version="1.0.0",
            endee_connected=endee_connected
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            service="Endee AI Knowledge Assistant",
            version="1.0.0",
            endee_connected=False
        )


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Process a user question through the RAG pipeline.
    
    Args:
        request: Question request with optional session ID.
        
    Returns:
        RAG pipeline response with answer and sources.
    """
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Check cache first
        cache = get_query_cache()
        cached_result = cache.get(request.question)
        if cached_result:
            logger.info(f"Returning cached result for: {request.question}")
            return JSONResponse(content=cached_result)
        
        # Start analytics
        analytics = get_analytics()
        start_time = analytics.record_query_start()
        
        # Optimize query
        optimizer = get_query_optimizer()
        validation = optimizer.validate_query(request.question)
        optimal_params = optimizer.get_optimal_parameters(request.question)
        
        pipeline = get_rag_pipeline()
        result = await pipeline.process_query(
            question=request.question,
            session_id=request.session_id,
            use_conversation_history=request.use_conversation_history
        )
        
        # Record analytics
        success = result.get("success", False)
        retrieved_count = result.get("retrieved_documents_count", 0)
        analytics.record_query_end(start_time, request.question, success, retrieved_count)
        
        # Cache successful results
        if success:
            cache.set(request.question, result)
        
        result["optimization"] = {
            "validation": validation,
            "optimal_parameters": optimal_params
        }
        
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        analytics = get_analytics()
        analytics.record_query_end(start_time, request.question, False, 0)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest")
async def ingest_documents(request: DocumentRequest):
    """Ingest documents into the vector database.
    
    Args:
        request: Document request with list of documents.
        
    Returns:
        Ingestion result with statistics.
    """
    try:
        if not request.documents:
            raise HTTPException(status_code=400, detail="No documents provided")
        
        pipeline = get_rag_pipeline()
        result = await pipeline.ingest_documents(
            documents=request.documents,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest/upload")
async def upload_and_ingest(
    file: UploadFile = File(...),
    source: Optional[str] = None
):
    """Upload and ingest a document file (PDF or TXT).
    
    Args:
        file: The file to upload.
        source: Optional source identifier.
        
    Returns:
        Ingestion result.
    """
    try:
        content = await file.read()
        source = source or file.filename
        
        # Handle PDF files
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Handle text files
        elif file.filename.endswith(('.txt', '.md')):
            text = content.decode('utf-8')
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Use PDF, TXT, or MD files."
            )
        
        pipeline = get_rag_pipeline()
        result = await pipeline.ingest_documents(
            documents=[{"text": text, "source": source}]
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session.
    
    Args:
        session_id: The session identifier.
        
    Returns:
        List of messages in the session.
    """
    try:
        from backend.memory_manager import get_session_manager
        
        session_manager = get_session_manager()
        session = session_manager.get_or_create_session(session_id)
        messages = session.get_messages()
        
        return {"session_id": session_id, "messages": messages}
    
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session.
    
    Args:
        session_id: The session identifier.
        
    Returns:
        Confirmation of deletion.
    """
    try:
        from backend.memory_manager import get_session_manager
        
        session_manager = get_session_manager()
        session_manager.delete_session(session_id)
        
        return {"message": f"Chat history cleared for session {session_id}"}
    
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/stats")
async def get_analytics_stats():
    """Get system analytics and statistics.
    
    Returns:
        Comprehensive system metrics and performance stats.
    """
    try:
        analytics = get_analytics()
        cache = get_query_cache()
        
        return {
            "system_stats": analytics.get_system_stats(),
            "cache_stats": cache.get_stats(),
            "recent_queries": analytics.get_recent_queries(5)
        }
    
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/report")
async def get_performance_report():
    """Get comprehensive performance report.
    
    Returns:
        Detailed performance metrics and insights.
    """
    try:
        analytics = get_analytics()
        return analytics.get_performance_report()
    
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cache/clear")
async def clear_cache():
    """Clear all query cache.
    
    Returns:
        Confirmation of cache clear.
    """
    try:
        cache = get_query_cache()
        cache.invalidate()
        return {"message": "Cache cleared successfully"}
    
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/optimize")
async def optimize_query(question: str):
    """Analyze and optimize a query.
    
    Args:
        question: The query to optimize.
        
    Returns:
        Query analysis and optimization recommendations.
    """
    try:
        optimizer = get_query_optimizer()
        
        validation = optimizer.validate_query(question)
        query_type = optimizer.detect_query_type(question)
        keywords = optimizer.extract_keywords(question)
        optimal_params = optimizer.get_optimal_parameters(question)
        preprocessed = optimizer.preprocess_query(question)
        
        return {
            "original_query": question,
            "preprocessed_query": preprocessed,
            "query_type": query_type,
            "keywords": keywords,
            "validation": validation,
            "optimal_parameters": optimal_params
        }
    
    except Exception as e:
        logger.error(f"Error optimizing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting up Endee AI Knowledge Assistant")
    
    try:
        endee_client = await get_endee_client()
        is_healthy = await endee_client.health_check()
        
        if is_healthy:
            logger.info("✓ Endee vector database is connected")
        else:
            logger.warning("⚠ Endee vector database is not responding")
    
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug
    )
