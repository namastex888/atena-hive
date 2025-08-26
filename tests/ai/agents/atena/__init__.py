"""
ATENA Educational AI Assistant Test Package

This package contains comprehensive test suites for the ATENA (Assistente Técnica Educacional em Algoritmos)
educational AI agent, implementing TDD methodology with failing tests first (RED phase).

Test Structure:
- test_atena_agent.py: Core agent functionality and integration tests
- test_pdf_processor.py: RAG-based PDF processing with performance validation
- test_educational_engine.py: Pedagogical interaction quality and concept explanation
- test_portuguese_nlp.py: Portuguese language processing for technical terminology
- test_progress_tracker.py: Student progress tracking using Agno memory system
- test_integration.py: End-to-end educational workflow integration tests
- test_performance.py: Performance validation for sub-3-second response requirement
- conftest.py: Shared fixtures and test configuration

All tests are designed to FAIL initially to ensure proper TDD RED phase compliance.
Implementation should be driven by making these failing tests pass (GREEN phase).
"""