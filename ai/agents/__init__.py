"""AI Agents Package"""

import importlib

# Import agent submodules using importlib for hyphenated names
template_agent = importlib.import_module('.template-agent', __name__)
tools = importlib.import_module('.tools', __name__)

# Make agent functions available at package level using importlib
template_agent_module = importlib.import_module('.template-agent', __name__)

# Extract agent functions
get_template_agent = template_agent_module.get_template_agent

__all__ = [
    # Submodules
    "template_agent",
    "tools",
    # Agent functions
    "get_template_agent",
]
