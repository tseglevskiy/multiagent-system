# Project Context Summary

This document provides a quick overview of the multi-agent system project for developers joining the project or returning after time away.

## 🎯 What This Project Is

A **multi-agent system demonstration** built with the Strands Agents framework, showcasing how a main orchestrator agent can coordinate two secondary agents using the Agent-to-Agent (A2A) protocol.

## 🏗️ Current State (v0.1.0)

### ✅ What's Complete
- **Project Foundation**: Modern Python setup with `uv` package manager
- **CLI Interface**: Professional command-line interface with Rich formatting
- **Documentation**: Comprehensive docs covering architecture, development, and deployment
- **Structure**: Clean, modular codebase ready for multi-agent implementation
- **Dependencies**: Strands Agents framework integrated and ready to use

### 🚧 What's Next (Phase 2)
- **Main Orchestrator Agent**: Workflow coordination and decision making
- **Data Processing Agent**: CSV analysis, statistics, data cleaning
- **Report Generation Agent**: PDF/HTML report creation with templates
- **A2A Communication**: Inter-agent communication protocol implementation

## 📁 Key Files to Know

### Documentation (Start Here)
- **`README.md`**: Project overview, setup, and usage examples
- **`DEVELOPMENT.md`**: Technical implementation details and patterns
- **`ARCHITECTURE.md`**: System design, data flow, and component relationships
- **`CHANGELOG.md`**: Version history and feature tracking

### Configuration
- **`pyproject.toml`**: Project dependencies and build configuration
- **`.env.example`**: Complete environment variable template
- **`multiagent_system/main.py`**: CLI entry point with Click commands

### Code Structure
```
multiagent_system/
├── agents/          # Future: Agent implementations
├── tools/           # Future: Custom tool definitions
└── main.py         # CLI interface (working)
```

## 🚀 Quick Start for Developers

```bash
# Get started immediately
cd multiagent-system
uv sync                    # Install dependencies
uv run multiagent hello    # Test the setup
uv run multiagent status   # Check system readiness

# View available commands
uv run multiagent --help
```

## 🎨 Design Philosophy

### Why Strands Agents?
- **A2A Protocol**: Standardized agent communication
- **AWS Integration**: Native Bedrock support
- **Production Focus**: Built for real-world deployment
- **Simplicity**: Less boilerplate than LangGraph/CrewAI

### Architecture Principles
- **Modular Design**: Each agent has specific responsibilities
- **Protocol-Based**: A2A for reliable inter-agent communication
- **Configuration-Driven**: Environment variables for all settings
- **Fault Tolerant**: Retry logic, timeouts, circuit breakers

## 🔧 Development Workflow

### Adding New Features
1. **Update Documentation**: Start with architecture/design docs
2. **Implement Core Logic**: Add agent or tool functionality
3. **Add CLI Commands**: Expose functionality through CLI
4. **Write Tests**: Unit and integration tests
5. **Update Changelog**: Document changes

### Code Organization
- **Agents**: Inherit from `BaseMultiAgent` class (to be created)
- **Tools**: Use `@tool` decorator from Strands framework
- **Configuration**: Pydantic models with environment variable support
- **CLI**: Click commands with Rich formatting

## 🎯 Success Metrics

### Technical Goals
- [ ] Main agent successfully coordinates 2+ secondary agents
- [ ] A2A protocol communication working reliably
- [ ] Error handling with graceful degradation
- [ ] Multiple LLM provider support (Bedrock, OpenAI, etc.)

### Quality Goals
- [ ] Comprehensive test coverage (>80%)
- [ ] Clear documentation for all components
- [ ] Production-ready configuration management
- [ ] Performance monitoring and logging

## 🔍 Debugging and Troubleshooting

### Common Issues
- **Import Errors**: Run `uv sync` to ensure dependencies are installed
- **CLI Not Working**: Check that `uv run multiagent` command works
- **Port Conflicts**: Agents use ports 9000-9002, ensure they're available

### Useful Commands
```bash
# Check project status
uv run multiagent status

# View project structure
find . -name "*.py" | grep -v .venv | sort

# Test basic functionality
uv run python main.py
```

## 📚 Learning Resources

### Framework-Specific
- [Strands Agents Docs](https://strandsagents.com/)
- [A2A Protocol Guide](https://google-a2a.github.io/A2A/latest/)
- [Strands Examples](https://github.com/strands-agents/samples)

### Multi-Agent Concepts
- Agent communication patterns
- Workflow orchestration strategies
- Distributed system design principles

## 🎯 Next Steps for New Developers

1. **Read the Documentation**: Start with README.md, then ARCHITECTURE.md
2. **Explore the Code**: Check out the CLI implementation in `main.py`
3. **Run the Examples**: Test the hello world functionality
4. **Review the Roadmap**: See CHANGELOG.md for planned features
5. **Set Up Environment**: Copy `.env.example` to `.env` and configure

## 💡 Key Insights from Development

### Framework Choice Rationale
- **Strands Agents** chosen over LangGraph/CrewAI for A2A protocol support
- **A2A Protocol** provides standardized agent communication
- **uv Package Manager** for faster dependency resolution
- **Rich CLI** for professional user experience

### Architecture Decisions
- **Port-Based Communication**: Each agent runs on separate port
- **Stateless Agents**: For horizontal scalability
- **Configuration-Driven**: All settings via environment variables
- **Modular Structure**: Clear separation of concerns

This project represents a modern approach to multi-agent systems with production-ready architecture and comprehensive documentation. The foundation is solid and ready for the next phase of development.
