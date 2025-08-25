# CLAUDE.md - Agents

🗺️ **Individual Agent Development Domain**

## 🧭 Navigation

**🔙 AI Hub**: [/ai/CLAUDE.md](../CLAUDE.md) | **🔙 Main**: [/CLAUDE.md](../../CLAUDE.md)  
**🔗 Related**: [Teams](../teams/CLAUDE.md) | [Workflows](../workflows/CLAUDE.md) | [Config](../../lib/config/CLAUDE.md) | [Knowledge](../../lib/knowledge/CLAUDE.md)

## Purpose

Template-based agent development framework. Use the template-agent structure as a starting point for creating new specialized agents.

## Agent Structure

**Template agent folder structure**:
```
template-agent/
├── agent.py      # Factory function with agent implementation
└── config.yaml   # Agent configuration and instructions
```

**Registry pattern**: `ai/agents/registry.py` loads all agents via factory functions

## Agent Development

**Agent Template**:
```python
def get_template_agent(**kwargs) -> Agent:
    config = yaml.safe_load(open("config.yaml"))
    
    return Agent(
        name=config["agent"]["name"],
        agent_id=config["agent"]["agent_id"],
        instructions=config["instructions"],
        tools=config.get("tools", []),
        model=ModelConfig(**config["model"]),
        storage=PostgresStorage(
            table_name=config["storage"]["table_name"],
            auto_upgrade_schema=True
        ),
        version="dev",  # All new agents use dev version
        **kwargs
    )
```

**Configuration Template**:
```yaml
agent:
  name: "Template Agent"
  agent_id: "template-agent"
  version: "dev"

model:
  provider: "anthropic"
  id: "claude-sonnet-4-20250514"
  temperature: 0.7

instructions: |
  You are a template agent for creating new specialized agents.
  
  Copy this structure and modify for your specific use case.

storage:
  table_name: "template_agent_sessions"
```

## Template Usage

**Creating New Agent:**
1. Copy `template-agent/` directory
2. Rename to your new agent name
3. Update `config.yaml` with agent-specific settings
4. Modify `agent.py` factory function
5. Add agent to registry

**Development Patterns:**
- Use template structure for consistency
- Follow factory pattern for agent creation  
- Store sessions in PostgreSQL
- Use structured configuration
- Test agent functionality

## Performance Targets

- **Response Time**: <2s agent responses
- **Memory**: Session state persistence
- **Storage**: PostgreSQL with auto-schema
- **Scalability**: Multiple concurrent agents