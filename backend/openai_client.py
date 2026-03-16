"""
OpenAI Integration Module

Handles embeddings generation and LLM completions using OpenAI API.
Uses GPT-4o mini for efficient and cost-effective responses.
"""

import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass
import os

try:
    from openai import AsyncOpenAI, OpenAI
except ImportError:
    raise ImportError("openai package required. Install with: pip install openai")

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingResult:
    """Result from embedding generation."""
    text: str
    embedding: List[float]
    model: str = "text-embedding-3-small"
    tokens_used: int = 0


@dataclass
class CompletionResult:
    """Result from LLM completion."""
    answer: str
    model: str = "gpt-4o-mini"
    tokens_used: int = 0
    stop_reason: str = "stop"


class OpenAIClient:
    """
    Complete OpenAI client for embeddings and LLM completions.
    
    Features:
    - Generate embeddings using text-embedding-3-small
    - Generate responses using gpt-4o-mini
    - Batch embeddings generation
    - Context-aware completions
    - Token usage tracking
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.async_client = AsyncOpenAI(api_key=self.api_key)
        
        # Models
        self.embedding_model = "text-embedding-3-small"
        self.completion_model = "gpt-4o-mini"
        
        # Embedding dimensions
        self.embedding_dimension = 1536
        
        logger.info(f"Initialized OpenAI client")
        logger.info(f"Embedding model: {self.embedding_model}")
        logger.info(f"Completion model: {self.completion_model}")
    
    def generate_embedding(self, text: str) -> EmbeddingResult:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            EmbeddingResult with embedding vector
        """
        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            # Clean text
            text = text.strip()[:8191]  # API limit
            
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            embedding = response.data[0].embedding
            tokens_used = response.usage.total_tokens
            
            logger.debug(f"Generated embedding (tokens: {tokens_used})")
            
            return EmbeddingResult(
                text=text,
                embedding=embedding,
                model=self.embedding_model,
                tokens_used=tokens_used
            )
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts (batch mode for efficiency).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of EmbeddingResult objects
        """
        try:
            if not texts:
                return []
            
            # Clean texts
            texts = [t.strip()[:8191] for t in texts if t.strip()]
            
            if not texts:
                return []
            
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            
            results = []
            for i, embedding_data in enumerate(response.data):
                results.append(
                    EmbeddingResult(
                        text=texts[i],
                        embedding=embedding_data.embedding,
                        model=self.embedding_model,
                        tokens_used=response.usage.total_tokens // len(texts)
                    )
                )
            
            logger.info(f"Generated {len(results)} embeddings (batch)")
            return results
            
        except Exception as e:
            logger.error(f"Error in batch embeddings: {str(e)}")
            raise
    
    async def generate_embedding_async(self, text: str) -> EmbeddingResult:
        """
        Async version of embedding generation.
        
        Args:
            text: Text to embed
            
        Returns:
            EmbeddingResult with embedding vector
        """
        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            text = text.strip()[:8191]
            
            response = await self.async_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            embedding = response.data[0].embedding
            tokens_used = response.usage.total_tokens
            
            return EmbeddingResult(
                text=text,
                embedding=embedding,
                model=self.embedding_model,
                tokens_used=tokens_used
            )
            
        except Exception as e:
            logger.error(f"Error in async embedding: {str(e)}")
            raise
    
    def generate_response(
        self,
        query: str,
        context: List[str],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> CompletionResult:
        """
        Generate a response using GPT-4o-mini with retrieved context.
        
        Args:
            query: User question
            context: Retrieved context chunks
            system_prompt: System prompt override
            temperature: Response temperature (0-1)
            max_tokens: Maximum response tokens
            
        Returns:
            CompletionResult with generated answer
        """
        try:
            if not system_prompt:
                system_prompt = self._get_default_system_prompt()
            
            # Build context string
            context_str = "\n\n".join(
                [f"Document {i+1}:\n{chunk}" for i, chunk in enumerate(context)]
            )
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""Based on the following context, answer the user's question.
If the answer cannot be found in the context, say "I don't have information about this."

Context:
{context_str}

Question: {query}"""
                }
            ]
            
            response = self.client.chat.completions.create(
                model=self.completion_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            stop_reason = response.choices[0].finish_reason
            
            logger.debug(f"Generated response (tokens: {tokens_used})")
            
            return CompletionResult(
                answer=answer,
                model=self.completion_model,
                tokens_used=tokens_used,
                stop_reason=stop_reason
            )
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    async def generate_response_async(
        self,
        query: str,
        context: List[str],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> CompletionResult:
        """
        Async version of response generation.
        
        Args:
            query: User question
            context: Retrieved context chunks
            system_prompt: System prompt override
            temperature: Response temperature
            max_tokens: Maximum response tokens
            
        Returns:
            CompletionResult with generated answer
        """
        try:
            if not system_prompt:
                system_prompt = self._get_default_system_prompt()
            
            context_str = "\n\n".join(
                [f"Document {i+1}:\n{chunk}" for i, chunk in enumerate(context)]
            )
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""Based on the following context, answer the user's question.
If the answer cannot be found in the context, say "I don't have information about this."

Context:
{context_str}

Question: {query}"""
                }
            ]
            
            response = await self.async_client.chat.completions.create(
                model=self.completion_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            stop_reason = response.choices[0].finish_reason
            
            return CompletionResult(
                answer=answer,
                model=self.completion_model,
                tokens_used=tokens_used,
                stop_reason=stop_reason
            )
            
        except Exception as e:
            logger.error(f"Error in async response generation: {str(e)}")
            raise
    
    def generate_response_stream(
        self,
        query: str,
        context: List[str],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Stream response generation for real-time UI updates.
        
        Args:
            query: User question
            context: Retrieved context chunks
            system_prompt: System prompt override
            temperature: Response temperature
            max_tokens: Maximum response tokens
            
        Yields:
            Response chunks as they're generated
        """
        try:
            if not system_prompt:
                system_prompt = self._get_default_system_prompt()
            
            context_str = "\n\n".join(
                [f"Document {i+1}:\n{chunk}" for i, chunk in enumerate(context)]
            )
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""Based on the following context, answer the user's question.
If the answer cannot be found in the context, say "I don't have information about this."

Context:
{context_str}

Question: {query}"""
                }
            ]
            
            with self.client.chat.completions.create(
                model=self.completion_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            ) as stream:
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
        except Exception as e:
            logger.error(f"Error in streaming response: {str(e)}")
            yield f"Error: {str(e)}"
    
    @staticmethod
    def _get_default_system_prompt() -> str:
        """Get the default system prompt for RAG."""
        return """You are a helpful AI assistant that answers questions based on provided documents.
You have access to relevant document excerpts to help answer the user's question.
Always cite which document(s) your answer comes from.
Be concise but thorough in your responses.
If information is not available in the provided context, clearly state that."""


# Singleton instance
_openai_client: Optional[OpenAIClient] = None


def get_openai_client(api_key: Optional[str] = None) -> OpenAIClient:
    """
    Get or create OpenAI client singleton.
    
    Args:
        api_key: OpenAI API key (optional)
        
    Returns:
        OpenAIClient instance
    """
    global _openai_client
    
    if _openai_client is None:
        _openai_client = OpenAIClient(api_key=api_key)
    
    return _openai_client
