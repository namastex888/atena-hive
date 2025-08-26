"""
Tests for error handlers module.
"""

import pytest
from unittest.mock import MagicMock, patch
import asyncio

from lib.utils.error_handlers import (
    APIKeyError,
    ModelProviderErrorHandler,
    handle_model_errors
)


class TestModelProviderErrorHandler:
    """Test the ModelProviderErrorHandler class."""
    
    def test_handle_api_key_expired_error(self):
        """Test handling of expired API key error."""
        handler = ModelProviderErrorHandler()
        
        # Create a mock error with API key expired message
        error = Exception("API key expired. Please renew the API key.")
        
        result = handler.handle_api_error(error, agent_id="test_agent")
        
        assert result["error"] == "authentication_error"
        assert "API key issue detected" in result["message"]
        assert result["agent"] == "test_agent"
        assert "Update your API key" in result["suggestion"]
    
    def test_handle_invalid_api_key_error(self):
        """Test handling of invalid API key error."""
        handler = ModelProviderErrorHandler()
        
        # Test with different API key error variations
        errors = [
            "API_KEY_INVALID",
            "Invalid API key provided",
            "Authentication failed",
            "Unauthorized access"
        ]
        
        for error_msg in errors:
            error = Exception(error_msg)
            result = handler.handle_api_error(error, agent_id="test_agent")
            
            assert result["error"] == "authentication_error"
            assert "API key issue" in result["message"]
    
    def test_handle_rate_limit_error(self):
        """Test handling of rate limit error."""
        handler = ModelProviderErrorHandler()
        
        error = Exception("Rate limit exceeded. Too many requests.")
        result = handler.handle_api_error(error, agent_id="test_agent")
        
        assert result["error"] == "rate_limit"
        assert "Rate limit reached" in result["message"]
        assert "Wait a few seconds" in result["suggestion"]
    
    def test_handle_model_not_found_error(self):
        """Test handling of model not found error."""
        handler = ModelProviderErrorHandler()
        
        error = Exception("Model not found: gpt-5")
        result = handler.handle_api_error(error, agent_id="test_agent")
        
        assert result["error"] == "model_not_found"
        assert "model is not available" in result["message"]
    
    def test_handle_generic_error(self):
        """Test handling of generic model provider error."""
        handler = ModelProviderErrorHandler()
        
        error = Exception("Some unexpected error occurred")
        result = handler.handle_api_error(error, agent_id="test_agent")
        
        assert result["error"] == "model_provider_error"
        assert "error occurred with the AI model provider" in result["message"]
        assert "Some unexpected error" in result["details"]


class TestHandleModelErrorsDecorator:
    """Test the handle_model_errors decorator."""
    
    @pytest.mark.asyncio
    async def test_async_function_with_model_error(self):
        """Test decorator on async function with model provider error."""
        
        # Create a mock error class
        class ModelProviderError(Exception):
            pass
        
        @handle_model_errors(agent_id="test_agent")
        async def failing_agent_func():
            # Raise a ModelProviderError
            raise ModelProviderError("API key expired")
        
        result = await failing_agent_func()
        
        assert result["success"] is False
        assert result["error"] == "authentication_error"
        assert result["agent"] == "test_agent"
    
    @pytest.mark.asyncio
    async def test_async_function_without_error(self):
        """Test decorator on async function that succeeds."""
        
        @handle_model_errors(agent_id="test_agent")
        async def successful_agent_func():
            return {"result": "success"}
        
        result = await successful_agent_func()
        
        assert result == {"result": "success"}
    
    @pytest.mark.asyncio
    async def test_async_function_with_non_model_error(self):
        """Test decorator re-raises non-model provider errors."""
        
        @handle_model_errors(agent_id="test_agent")
        async def failing_func():
            raise ValueError("This is not a model error")
        
        with pytest.raises(ValueError):
            await failing_func()
    
    def test_sync_function_with_model_error(self):
        """Test decorator on sync function with model provider error."""
        
        # Create a mock error class
        class APIError(Exception):
            pass
        
        @handle_model_errors(agent_id="test_agent")
        def failing_agent_func():
            # Raise an APIError
            raise APIError("Authentication failed")
        
        result = failing_agent_func()
        
        assert result["success"] is False
        assert result["error"] == "authentication_error"
    
    def test_sync_function_without_error(self):
        """Test decorator on sync function that succeeds."""
        
        @handle_model_errors(agent_id="test_agent")
        def successful_func():
            return {"result": "success"}
        
        result = successful_func()
        
        assert result == {"result": "success"}


class TestAPIKeyError:
    """Test the custom APIKeyError exception."""
    
    def test_api_key_error_creation(self):
        """Test that APIKeyError can be created and raised."""
        with pytest.raises(APIKeyError) as exc_info:
            raise APIKeyError("Invalid API key")
        
        assert str(exc_info.value) == "Invalid API key"