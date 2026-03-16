"""Script for batch ingesting documents into the knowledge base."""
import asyncio
import json
import os
from pathlib import Path
import requests
from typing import List, Dict

# Backend configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
INGEST_ENDPOINT = f"{BACKEND_URL}/ingest"
UPLOAD_ENDPOINT = f"{BACKEND_URL}/ingest/upload"


def load_sample_documents() -> List[Dict[str, str]]:
    """Load sample documents for demonstration."""
    sample_docs = [
        {
            "text": """# Endee Vector Database Guide

Endee is an open-source vector database designed for high-performance similarity search and RAG (Retrieval Augmented Generation) pipelines.

## Key Features
- Ultra-fast semantic search capabilities
- Efficient vector storage and retrieval
- Support for filtered vector search
- Scalable architecture for large datasets
- RESTful API for easy integration

## Installation
The Endee database can be installed using the provided install script:

chmod +x install.sh run.sh
./install.sh --release --avx2
./run.sh

The server will start on http://localhost:8080

## REST API Endpoints
- POST /collections - Create a new collection
- POST /upsert - Upsert vectors into a collection
- POST /search - Perform similarity search
- DELETE /collections/{name} - Delete a collection
- GET /health - Check server health

## Use Cases
1. Semantic Search - Find similar documents using embeddings
2. RAG Pipelines - Retrieve relevant context for LLMs
3. Recommendation Systems - Find similar items
4. Question Answering - Match questions to answers
5. Content Discovery - Find related content
""",
            "source": "Endee Documentation"
        },
        {
            "text": """# Getting Started with Vector Embeddings

Vector embeddings are numerical representations of text that capture semantic meaning. They enable machines to understand and compare the similarity of text.

## What are Embeddings?
Embeddings convert text into fixed-size vectors of numbers. Similar texts have similar embeddings, making it possible to find related content using distance metrics.

## Popular Embedding Models
1. sentence-transformers/all-MiniLM-L6-v2 - Fast, lightweight, 384 dimensions
2. OpenAI text-embedding-3-small - High quality, commercial
3. Google's Universal Sentence Encoder - Versatile, good for many tasks
4. Cohere embeddings - Advanced, tuned for enterprise use

## Why Use Embeddings?
- Enable semantic search beyond keyword matching
- Support recommendation systems
- Enable RAG (Retrieval Augmented Generation)
- Power similarity matching and clustering
- Enable natural language queries

## Best Practices
1. Use consistent embedding models
2. Normalize embeddings for cosine similarity
3. Store metadata with embeddings
4. Update embeddings when data changes
5. Monitor embedding quality and relevance
""",
            "source": "AI Fundamentals Guide"
        },
        {
            "text": """# RAG (Retrieval Augmented Generation) Systems

RAG combines the power of large language models with the ability to retrieve relevant information from external sources.

## How RAG Works
1. User asks a question
2. System retrieves relevant documents from vector database
3. Retrieved documents are used as context
4. LLM generates an answer based on the context
5. Answer is provided to the user with source citations

## Advantages of RAG
- Provides current, factual information
- Reduces hallucination in LLM responses
- Enables knowledge base integration
- Improves answer accuracy and relevance
- Allows source attribution

## Building RAG Pipelines
Key components:
1. Document storage and indexing
2. Vector database for embeddings
3. Embedding model for queries
4. LLM for answer generation
5. Retrieval and ranking mechanism

## Real-World Applications
- Customer support automation
- Knowledge base search
- Research assistance
- Documentation QA
- Corporate knowledge systems
""",
            "source": "RAG Architecture Guide"
        },
        {
            "text": """# Multi-Agent AI Systems

Multi-agent systems coordinate multiple AI agents to solve complex problems.

## What are AI Agents?
An AI agent is an autonomous system that:
- Perceives its environment
- Makes decisions
- Takes actions
- Learns from results

## Types of Agents
1. Query Understanding Agents - Parse and optimize user input
2. Retrieval Agents - Fetch relevant information
3. Reasoning Agents - Process and reason over data
4. Response Agents - Format and present results
5. Planning Agents - Orchestrate complex workflows

## Benefits of Multi-Agent Systems
- Divide complex problems into manageable tasks
- Improve specialized performance
- Enable parallel processing
- Support error recovery
- Allow knowledge specialization

## Challenges
- Agent coordination complexity
- Communication overhead
- State management
- Testing and debugging
- Scalability considerations

## Implementation Tips
1. Define clear agent responsibilities
2. Use message-based communication
3. Implement proper error handling
4. Monitor agent performance
5. Test agent interactions thoroughly
""",
            "source": "Multi-Agent Systems Guide"
        },
        {
            "text": """# FastAPI Best Practices

FastAPI is a modern Python web framework for building APIs with automatic documentation.

## Project Structure
A well-organized FastAPI project should have:
- main.py - Application entry point
- config.py - Configuration management
- routers/ - Route handlers
- models/ - Pydantic models
- services/ - Business logic
- utils/ - Helper functions

## Key Features
1. Automatic API documentation (Swagger, ReDoc)
2. Built-in data validation with Pydantic
3. Dependency injection system
4. Async/await support
5. Security features

## Common Patterns
1. Dependency Injection - Use dependency() for DI
2. Middleware - Add cross-cutting concerns
3. Exception Handling - Use HTTPException for errors
4. CORS - Configure for frontend integration
5. Authentication - Use OAuth2, JWT tokens

## Performance Tips
1. Use async functions where possible
2. Implement caching strategies
3. Use connection pooling
4. Optimize database queries
5. Monitor application performance

## Deployment
- Use Gunicorn with Uvicorn workers
- Enable HTTPS/SSL
- Set proper environment variables
- Use health check endpoints
- Implement proper logging
""",
            "source": "FastAPI Guide"
        }
    ]
    
    return sample_docs


def ingest_documents(documents: List[Dict[str, str]]) -> Dict:
    """Ingest documents via the REST API.
    
    Args:
        documents: List of documents to ingest
        
    Returns:
        Response from the backend
    """
    try:
        payload = {
            "documents": documents,
            "chunk_size": 500,
            "chunk_overlap": 50
        }
        
        response = requests.post(INGEST_ENDPOINT, json=payload, timeout=120)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return {"success": False, "error": response.text}
    
    except Exception as e:
        print(f"Error during ingestion: {str(e)}")
        return {"success": False, "error": str(e)}


def ingest_file(file_path: str, source_name: str = None) -> Dict:
    """Ingest a document file.
    
    Args:
        file_path: Path to the document file
        source_name: Optional source identifier
        
    Returns:
        Response from the backend
    """
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return {"success": False, "error": "File not found"}
        
        with open(file_path, 'rb') as f:
            files = {"file": (Path(file_path).name, f)}
            params = {}
            if source_name:
                params["source"] = source_name
            
            response = requests.post(
                UPLOAD_ENDPOINT,
                files=files,
                params=params,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return {"success": False, "error": response.text}
    
    except Exception as e:
        print(f"Error during file ingestion: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    """Main function for batch ingestion."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ingest documents into the Endee knowledge base"
    )
    parser.add_argument(
        "--mode",
        choices=["sample", "file", "directory"],
        default="sample",
        help="Ingestion mode"
    )
    parser.add_argument(
        "--path",
        help="Path to file or directory (for file/directory modes)"
    )
    parser.add_argument(
        "--source",
        help="Source name for the documents"
    )
    
    args = parser.parse_args()
    
    print("🚀 Starting document ingestion...")
    print(f"Backend URL: {BACKEND_URL}")
    
    if args.mode == "sample":
        print("\n📚 Loading sample documents...")
        documents = load_sample_documents()
        print(f"Loaded {len(documents)} sample documents")
        
        print("\n⏳ Ingesting documents...")
        result = ingest_documents(documents)
        
        if result.get("success"):
            print(f"✓ Success!")
            print(f"  - Documents ingested: {result.get('documents_ingested')}")
            print(f"  - Chunks created: {result.get('chunks_created')}")
            print(f"  - Vectors stored: {result.get('vectors_stored')}")
        else:
            print(f"✗ Failed: {result.get('error')}")
    
    elif args.mode == "file":
        if not args.path:
            print("Error: --path required for file mode")
            return
        
        print(f"\n📄 Ingesting file: {args.path}")
        result = ingest_file(args.path, args.source)
        
        if result.get("success"):
            print(f"✓ Success!")
            print(f"  - Documents ingested: {result.get('documents_ingested')}")
            print(f"  - Chunks created: {result.get('chunks_created')}")
            print(f"  - Vectors stored: {result.get('vectors_stored')}")
        else:
            print(f"✗ Failed: {result.get('error')}")
    
    elif args.mode == "directory":
        if not args.path:
            print("Error: --path required for directory mode")
            return
        
        print(f"\n📂 Scanning directory: {args.path}")
        
        supported_extensions = ['.pdf', '.txt', '.md']
        files = []
        for ext in supported_extensions:
            files.extend(Path(args.path).glob(f"*{ext}"))
        
        if not files:
            print("No supported files found in directory")
            return
        
        print(f"Found {len(files)} files to ingest")
        
        for file_path in files:
            print(f"\n  ➜ {file_path.name}")
            result = ingest_file(str(file_path), args.source or file_path.stem)
            if result.get("success"):
                print(f"    ✓ Success")
            else:
                print(f"    ✗ Failed: {result.get('error')}")
    
    print("\n✅ Ingestion complete!")


if __name__ == "__main__":
    main()
