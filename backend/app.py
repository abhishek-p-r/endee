"""
FastAPI Application for Endee RAG System

Complete REST API for document ingestion, semantic search, and answer generation
using Endee vector database and OpenAI models.
"""

import logging
import os
from typing import List, Optional
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

from backend.endee_vector_db import get_endee_client, EndeeVectorDB
from backend.openai_client import get_openai_client, OpenAIClient
from backend.rag_system import get_rag_system, RAGSystem
from backend.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
endee_db: Optional[EndeeVectorDB] = None
openai_client: Optional[OpenAIClient] = None
rag_system: Optional[RAGSystem] = None


# ============================================================================
# Request/Response Models
# ============================================================================

class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str
    top_k: Optional[int] = 5
    min_score: Optional[float] = 0.3


class DocumentUploadRequest(BaseModel):
    """Request model for document upload."""
    filename: str
    content: str


class IngestRequest(BaseModel):
    """Request model for document ingestion."""
    file_paths: List[str]
    chunk_size: Optional[int] = 500
    chunk_overlap: Optional[int] = 50


class QueryOptimizeRequest(BaseModel):
    """Request model for query optimization."""
    query: str


# ============================================================================
# Lifecycle Management
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    logger.info("Starting Endee RAG API Server...")
    
    global endee_db, openai_client, rag_system
    
    try:
        # Initialize Endee client
        endee_db = await get_endee_client(
            host=os.getenv("ENDEE_HOST", "localhost"),
            port=int(os.getenv("ENDEE_PORT", "8000"))
        )
        
        # Check Endee health
        is_healthy = await endee_db.health_check()
        if not is_healthy:
            logger.warning("Endee server is not responding")
        
        # Initialize OpenAI client
        openai_client = get_openai_client()
        logger.info("OpenAI client initialized")
        
        # Initialize RAG system
        rag_system = await get_rag_system(endee_db, openai_client)
        logger.info("RAG system initialized")
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    if endee_db:
        await endee_db.close()
    logger.info("Shutdown complete")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Endee RAG System API",
    description="AI-powered RAG system using Endee vector database and OpenAI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Check system health status."""
    try:
        endee_health = await endee_db.health_check() if endee_db else False
        
        return {
            "status": "healthy",
            "endee_connected": endee_health,
            "openai_configured": openai_client is not None,
            "rag_ready": rag_system is not None
        }
    
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def system_stats():
    """Get system statistics."""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        stats = await rag_system.get_stats()
        return stats
    
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Document Management Endpoints
# ============================================================================

@app.post("/ingest")
async def ingest_documents(request: IngestRequest, background_tasks: BackgroundTasks):
    """
    Ingest documents into the RAG system.
    
    Process documents, generate embeddings, and store in Endee vector database.
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        if not request.file_paths:
            raise HTTPException(status_code=400, detail="No file paths provided")
        
        logger.info(f"Starting ingestion of {len(request.file_paths)} files")
        
        result = await rag_system.ingest_documents(request.file_paths)
        
        return result
    
    except Exception as e:
        logger.error(f"Ingestion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a single document.
    
    Supports .txt, .pdf, and .md files.
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        # Save uploaded file
        upload_dir = "/tmp/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Uploaded file: {file.filename}")
        
        # Ingest the document
        result = await rag_system.ingest_documents([file_path])
        
        return result
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RAG Query Endpoints
# ============================================================================

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an answer from the RAG system.
    
    Retrieves relevant documents and generates answer using OpenAI.
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing question: {request.question[:100]}...")
        
        response = await rag_system.answer_question(
            query=request.question,
            top_k=request.top_k
        )
        
        return response.to_dict()
    
    except Exception as e:
        logger.error(f"Question error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def semantic_search(request: QuestionRequest):
    """
    Perform semantic search in the vector database.
    
    Returns relevant documents without generating an answer.
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        logger.info(f"Semantic search: {request.question[:100]}...")
        
        results = await rag_system.retrieve(
            query=request.question,
            top_k=request.top_k,
            min_score=request.min_score
        )
        
        search_results = [
            {
                "id": r.id,
                "score": r.score,
                "text": r.text,
                "metadata": r.metadata
            }
            for r in results
        ]
        
        return {
            "query": request.question,
            "results_count": len(search_results),
            "results": search_results
        }
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stream")
async def stream_answer(request: QuestionRequest):
    """
    Stream answer generation for real-time UI updates.
    
    Returns streaming response chunks.
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        async def generate():
            try:
                async for chunk in rag_system.stream_answer(
                    query=request.question,
                    top_k=request.top_k
                ):
                    yield chunk
            except Exception as e:
                logger.error(f"Stream error: {str(e)}")
                yield f"Error: {str(e)}"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    except Exception as e:
        logger.error(f"Streaming error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Optimization Endpoints
# ============================================================================

@app.post("/optimize-query")
async def optimize_query(request: QueryOptimizeRequest):
    """
    Analyze and optimize a query for better retrieval.
    
    Provides suggestions for query improvement.
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Basic query optimization
        original = request.query
        optimized = original.strip().lower()
        
        # Extract key terms
        words = optimized.split()
        keywords = [w for w in words if len(w) > 3]
        
        return {
            "original_query": original,
            "optimized_query": optimized,
            "keywords": keywords,
            "query_length": len(words),
            "suggestions": [
                "Use specific keywords",
                "Keep query concise",
                "Remove stop words",
                "Use clear questions"
            ]
        }
    
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Vector Database Management Endpoints
# ============================================================================

@app.get("/vectors/stats")
async def vector_stats():
    """Get vector database statistics."""
    try:
        if not endee_db:
            raise HTTPException(status_code=503, detail="Vector DB not initialized")
        
        stats = await endee_db.get_collection_stats()
        return stats
    
    except Exception as e:
        logger.error(f"Vector stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vectors/clear")
async def clear_vectors():
    """Clear all vectors from the database."""
    try:
        if not endee_db:
            raise HTTPException(status_code=503, detail="Vector DB not initialized")
        
        success = await endee_db.clear_collection()
        
        if success:
            return {"message": "Vectors cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear vectors")
    
    except Exception as e:
        logger.error(f"Clear vectors error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Endee RAG System API",
        "version": "1.0.0",
        "description": "AI-powered RAG system using Endee vector database and OpenAI",
        "endpoints": {
            "health": "/health",
            "stats": "/stats",
            "docs": "/docs",
            "ingest": "POST /ingest",
            "upload": "POST /upload",
            "ask": "POST /ask",
            "search": "POST /search",
            "stream": "POST /stream"
        }
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "backend.app:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
