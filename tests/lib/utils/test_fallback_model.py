"""
Tests for FallbackModel error handling.

Tests the fallback model that provides graceful error handling
when API keys are invalid or other provider errors occur.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

from lib.utils.fallback_model import FallbackModel


class TestFallbackModel:
    """Test suite for FallbackModel."""
    
    @pytest.fixture
    def api_key_error_response(self):
        """Mock error response for API key issues."""
        return {
            "error": "authentication_error",
            "message": "⚠️ API key issue detected. Please check your API credentials in the .env file.",
            "details": "The API key for this model provider is either expired, invalid, or missing.",
            "agent": "test-agent",
            "suggestion": "Update your API key in the .env file and restart the server."
        }
    
    @pytest.fixture
    def rate_limit_error_response(self):
        """Mock error response for rate limit issues."""
        return {
            "error": "rate_limit",
            "message": "⏱️ Rate limit reached. Please try again in a moment.",
            "agent": "test-agent",
            "suggestion": "Wait a few seconds before retrying."
        }
    
    @pytest.fixture
    def fallback_model(self, api_key_error_response):
        """Create a FallbackModel instance for testing."""
        return FallbackModel(
            error_response=api_key_error_response,
            component_id="test-agent"
        )
    
    def test_fallback_model_creation(self, api_key_error_response):
        """Test FallbackModel can be created with error response."""
        model = FallbackModel(
            error_response=api_key_error_response,
            component_id="test-agent"
        )
        
        assert model.error_response == api_key_error_response
        assert model.component_id == "test-agent"
        assert model.id == "fallback-test-agent"
        assert model.provider == "fallback"
    
    def test_invoke_returns_error_message(self, fallback_model):
        """Test that invoke returns formatted error message."""
        result = fallback_model.invoke("test message")
        
        assert isinstance(result, str)
        assert "Authentication Error" in result
        assert "API key issue detected" in result
        assert "test-agent" in result
        assert "Update your API key" in result
    
    @pytest.mark.asyncio
    async def test_ainvoke_returns_error_message(self, fallback_model):
        """Test that async invoke returns formatted error message."""
        result = await fallback_model.ainvoke("test message")
        
        assert isinstance(result, str)
        assert "Authentication Error" in result
        assert "API key issue detected" in result
        assert "test-agent" in result
    
    def test_stream_yields_error_chunks(self, fallback_model):
        """Test that stream yields error message in chunks."""
        chunks = list(fallback_model.stream("test message"))
        
        assert len(chunks) > 0
        full_message = "".join(chunks)
        assert "Authentication Error" in full_message
        assert "API key issue detected" in full_message
    
    @pytest.mark.asyncio
    async def test_astream_yields_error_chunks(self, fallback_model):
        """Test that async stream yields error message in chunks."""
        chunks = []
        async for chunk in fallback_model.astream("test message"):
            chunks.append(chunk)
        
        assert len(chunks) > 0
        full_message = "".join(chunks)
        assert "Authentication Error" in full_message
        assert "API key issue detected" in full_message
    
    def test_format_error_message_with_api_key_error(self, api_key_error_response):
        """Test error message formatting for API key errors."""
        model = FallbackModel(api_key_error_response, "test-agent")
        message = model._format_error_message()
        
        assert "Authentication Error" in message
        assert "API key issue detected" in message
        assert "Update your API key" in message
        assert "test-agent" in message
        assert "fallback mode" in message
    
    def test_format_error_message_with_rate_limit_error(self, rate_limit_error_response):
        """Test error message formatting for rate limit errors."""
        model = FallbackModel(rate_limit_error_response, "test-agent")
        message = model._format_error_message()
        
        assert "Rate Limit" in message
        assert "Rate limit reached" in message
        assert "Wait a few seconds" in message
        assert "test-agent" in message
    
    def test_model_properties(self, fallback_model):
        """Test model properties are accessible."""
        assert fallback_model.model_name == "fallback-test-agent"
        assert fallback_model.model_id == "fallback-test-agent"
        assert str(fallback_model) == "FallbackModel(test-agent)"
        assert "FallbackModel(component_id='test-agent'" in repr(fallback_model)
    
    def test_handles_missing_error_fields(self):
        """Test FallbackModel handles missing fields in error response."""
        minimal_error = {
            "error": "unknown_error"
        }
        
        model = FallbackModel(minimal_error, "test-agent")
        message = model._format_error_message()
        
        assert "Unknown Error" in message
        assert "An unknown error occurred" in message
        assert "test-agent" in message
    
    @pytest.mark.asyncio
    async def test_preserves_api_compatibility(self, fallback_model):
        """Test that FallbackModel maintains API compatibility with real models."""
        # Test synchronous invoke
        sync_result = fallback_model.invoke(["role: user", "content: test"])
        assert isinstance(sync_result, str)
        
        # Test asynchronous invoke
        async_result = await fallback_model.ainvoke({"role": "user", "content": "test"})
        assert isinstance(async_result, str)
        
        # Test streaming
        stream_chunks = list(fallback_model.stream("test input"))
        assert len(stream_chunks) > 0
        
        # Test async streaming
        astream_chunks = []
        async for chunk in fallback_model.astream("test input"):
            astream_chunks.append(chunk)
        assert len(astream_chunks) > 0