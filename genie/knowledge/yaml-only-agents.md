# YAML-Only Agent Pattern

## Overview
Agents can be created using only YAML configuration without requiring custom Python code. The proxy system automatically handles all Agno framework integration.

## How It Works

### 1. Create Agent Directory
```bash
mkdir ai/agents/my-agent
```

### 2. Create config.yaml
```yaml
agent:
  name: "My Agent Name"
  agent_id: "my-agent"
  version: 1
  description: "Agent description"

model:
  id: "claude-sonnet-4-20250514"  # or any supported model
  provider: "anthropic"
  temperature: 0.7
  max_tokens: 4096

storage:
  type: "postgres"
  table_name: "my_agent_sessions"
  auto_upgrade_schema: true

memory:
  enable_user_memories: true
  enable_agentic_memory: true
  num_history_runs: 10

display:
  markdown: true
  show_tool_calls: true
  add_datetime_to_instructions: true

instructions: |
  You are a helpful assistant.
  Your role is to help users with their tasks.

tools: []  # Add tools if needed
```

### 3. That's It!
The agent will automatically be discovered and loaded by the registry. No Python code required!

## Supported Sections

- **agent**: Core metadata (name, id, version, description)
- **model**: LLM configuration (provider, model ID, parameters)
- **storage**: Session persistence (postgres, sqlite, etc.)
- **memory**: Conversation memory settings
- **display**: Output formatting preferences
- **context**: Context injection settings
- **events**: Event tracking configuration
- **streaming**: Response streaming settings
- **tools**: List of tools/functions the agent can use
- **instructions**: System prompt/instructions
- **expected_output**: Expected response format
- **success_criteria**: Quality criteria

## Advanced: Custom Logic (Optional)

If you need custom logic, create an `agent.py` file:

```python
from agno.agent import Agent

def get_my_agent() -> Agent:
    # Custom initialization logic here
    return Agent.from_yaml("config.yaml")
```

## Benefits

1. **Simplicity**: No code needed for standard agents
2. **Consistency**: All agents follow same structure
3. **Maintainability**: Configuration changes don't require code changes
4. **Discovery**: Agents are automatically discovered by the registry
5. **Flexibility**: Can add custom logic when needed

## Example: Educational Assistant

See `ai/agents/atena/config.yaml` for a complete example of a YAML-only agent that provides educational assistance in Portuguese.

## Troubleshooting

If your agent isn't working:

1. Check that config.yaml has proper YAML syntax
2. Ensure agent_id in config matches directory name
3. Verify model provider credentials are in .env
4. Check logs for specific error messages