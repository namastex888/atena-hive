# CLAUDE.md - AI Domain

🗺️ **Multi-Agent System Orchestration Domain**

## 🧭 Navigation

**🔙 Main Hub**: [/CLAUDE.md](../CLAUDE.md)  
**🎯 AI Sub-areas**: [agents/](agents/CLAUDE.md) | [teams/](teams/CLAUDE.md) | [workflows/](workflows/CLAUDE.md)  
**🔗 Integration**: [API](../api/CLAUDE.md) | [Config](../lib/config/CLAUDE.md) | [Knowledge](../lib/knowledge/CLAUDE.md)

## Multi-Agent System Structure

**Template-Based Development:**
```
🏗️ TEMPLATES (ai/agents/, ai/teams/, ai/workflows/)
    ├── template-agent → Agent template structure
    ├── template-team → Team template structure
    ├── template-workflow → Workflow template structure
    └── template-tool → Tool template structure
```

## Development Patterns

**Agent Creation Flow:**
- **Copy Template** → Use template-agent as starting point
- **Customize Config** → Update agent-specific settings
- **Implement Logic** → Add specialized functionality
- **Add to Registry** → Include in agent discovery
- **Test Integration** → Verify agent functionality

## Quick Patterns

### Agent Creation
```bash
cp -r ai/agents/template-agent ai/agents/my-agent
# Edit config.yaml, bump version, implement factory function
```

### Team Creation
```bash
cp -r ai/teams/template-team ai/teams/my-team
# Edit config.yaml, define members and routing logic
```

### Workflow Creation  
```bash
cp -r ai/workflows/template-workflow ai/workflows/my-workflow
# Edit config.yaml, define steps and coordination
```

### Workflow Steps
```python
workflow = Workflow(steps=[
    Step("Analysis", team=analysis_team),
    Parallel(
        Step("Testing", agent=qa_agent),
        Step("Docs", agent=doc_agent)
    )
])
```

## Integration Points

- **🏗️ Templates**: Copy-and-modify pattern for all components
- **🌐 API**: Auto-expose via `Playground(agents, teams, workflows)`
- **🔧 Config**: YAML-first configs, environment scaling  
- **🧠 Knowledge**: CSV-RAG with domain filtering
- **🔐 Auth**: User context + session state
- **📊 Logging**: Structured logging with emoji prefixes

## Performance Targets

- **Agents**: <2s response time
- **Teams**: <5s routing decisions
- **Workflows**: <30s complex processes
- **Scale**: 1000+ concurrent users

## Critical Rules

- **🚨 Version Bump**: ANY change requires YAML version increment
- **Factory Pattern**: Use registry-based component creation
- **YAML-First**: Never hardcode - use configs + .env
- **Testing Required**: Every component needs tests
- **No Backward Compatibility**: Break cleanly for modern implementations

**Deep Dive**: Navigate to [agents/](agents/CLAUDE.md), [teams/](teams/CLAUDE.md), or [workflows/](workflows/CLAUDE.md) for implementation details.