"""
Tests for Atena Educational Agent
"""

import pytest
from ai.agents.atena.agent import get_atena_agent


def test_get_atena_agent():
    """Test that we can create the Atena agent"""
    agent = get_atena_agent()
    assert agent is not None
    assert agent.agent_id == "atena"
    assert "Atena" in agent.name


def test_agent_model_configuration():
    """Test that agent uses Gemini-2.5-pro with url_context"""
    agent = get_atena_agent()
    assert agent.model.id == "gemini-2.5-pro"
    # Check that instructions contain Portuguese content
    assert "Você é a ATENA" in agent.instructions


def test_agent_pdf_context():
    """Test that agent includes PDF URLs in instructions"""
    agent = get_atena_agent()
    # Check that PDFs are referenced
    assert "I_Teórico.docx.pdf" in agent.instructions
    assert "II_Teórico.docx.pdf" in agent.instructions
    assert "III_Teórico.docx.pdf" in agent.instructions
    assert "IV_Teórico.docx.pdf" in agent.instructions