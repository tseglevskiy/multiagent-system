# Multi-Agent System with Strands Agents

A comprehensive Python project demonstrating multi-agent systems using the Strands Agents framework. This project implements a main orchestrator agent that coordinates two secondary agents using the Agent-to-Agent (A2A) protocol.

## 🎯 Project Overview

This project was created to explore multi-agent architectures where:
- A **Main Orchestrator Agent** coordinates the overall workflow
- A **Data Processing Agent** handles data analysis tasks
- A **Report Generation Agent** creates reports from processed data
- All agents communicate via the standardized A2A protocol

### Why Strands Agents?

Strands Agents was chosen over alternatives like LangGraph, CrewAI, or AutoGen because:
- **Model-Driven Approach**: Simple, lightweight framework with minimal boilerplate
- **A2A Protocol**: Standardized agent communication over HTTP
- **AWS Integration**: Excellent support for Amazon Bedrock and other AWS services
- **Production-Ready**: Built with deployment and scaling considerations
- **MCP Support**: Native Model Context Protocol integration for tool access

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- `uv` package manager (recommended for fast dependency management)

### Installation
```bash
# Clone and navigate to project
cd multiagent-system

# Install dependencies
uv sync

# Test the setup
uv run multiagent hello
```

### Available Commands
```bash
# Simple hello world
uv run python main.py

# CLI interface with Rich formatting
uv run multiagent hello          # Welcome message
uv run multiagent status         # System status
uv run multiagent --help         # Show all commands

# Future multi-agent commands (to be implemented)
uv run multiagent run            # Execute multi-agent workflow
uv run multiagent agents list    # List available agents
uv run multiagent config         # Configure LLM providers
```

## 📁 Project Structure

```
multiagent-system/
├── multiagent_system/              # Main Python package
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # CLI entry point with Click & Rich
│   ├── agents/                     # Agent implementations
│   │   ├── __init__.py
│   │   ├── main_agent.py          # Main orchestrator (TODO)
│   │   ├── data_agent.py          # Data processing agent (TODO)
│   │   └── report_agent.py        # Report generation agent (TODO)
│   ├── tools/                     # Custom tools and utilities
│   │   ├── __init__.py
│   │   └── custom_tools.py        # Custom tool implementations (TODO)
│   ├── config/                    # Configuration management (TODO)
│   │   ├── __init__.py
│   │   ├── settings.py            # Application settings
│   │   └── models.py              # LLM model configurations
│   └── utils/                     # Utility functions (TODO)
│       ├── __init__.py
│       └── helpers.py             # Helper functions
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_agents/               # Agent tests (TODO)
│   ├── test_tools/                # Tool tests (TODO)
│   └── test_integration/          # Integration tests (TODO)
├── examples/                      # Usage examples (TODO)
│   ├── basic_workflow.py          # Simple multi-agent example
│   └── advanced_workflow.py       # Complex coordination example
├── docs/                          # Additional documentation (TODO)
│   ├── architecture.md            # System architecture
│   ├── deployment.md              # Deployment guide
│   └── api.md                     # API documentation
├── main.py                        # Simple hello world entry point
├── pyproject.toml                 # Project configuration & dependencies
├── README.md                      # This file
└── .env.example                   # Environment variables template (TODO)
```

## 🏗️ Architecture Design

### Agent Communication Flow
```
┌─────────────────┐    A2A Protocol    ┌─────────────────┐
│   Main Agent    │◄──────────────────►│   Data Agent    │
│  (Orchestrator) │                    │  (Processor)    │
└─────────┬───────┘                    └─────────────────┘
          │
          │ A2A Protocol
          ▼
┌─────────────────┐
│  Report Agent   │
│  (Generator)    │
└─────────────────┘
```

### Technology Stack
- **Framework**: Strands Agents (v0.1.9+)
- **Protocol**: Agent-to-Agent (A2A) for inter-agent communication
- **CLI**: Click + Rich for beautiful command-line interface
- **Package Manager**: uv for fast dependency resolution
- **LLM Support**: Amazon Bedrock, OpenAI, Anthropic, Ollama, etc.
- **Tools**: MCP (Model Context Protocol) integration

## 🔧 Dependencies

### Core Dependencies
```toml
strands-agents = ">=0.1.0"          # Main framework
strands-agents-tools = ">=0.1.0"    # Pre-built tools
click = ">=8.0.0"                   # CLI framework
rich = ">=13.0.0"                   # Terminal formatting
```

### Development Dependencies (Future)
- `pytest` - Testing framework
- `black` - Code formatting
- `ruff` - Linting
- `mypy` - Type checking

## 🎯 Implementation Roadmap

### Phase 1: Foundation (✅ Complete)
- [x] Project structure setup with uv
- [x] Basic CLI interface with Rich
- [x] Strands Agents integration
- [x] Hello world functionality

### Phase 2: Core Agents (🚧 Next)
- [ ] Implement Main Orchestrator Agent
- [ ] Create Data Processing Agent with custom tools
- [ ] Build Report Generation Agent
- [ ] Set up A2A protocol communication

### Phase 3: Advanced Features
- [ ] Configuration management for multiple LLM providers
- [ ] Custom tool development and integration
- [ ] Error handling and retry mechanisms
- [ ] Logging and monitoring

### Phase 4: Production Ready
- [ ] Comprehensive testing suite
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Documentation and examples

## 🛠️ Development Context

### Key Design Decisions
1. **Strands Agents over alternatives**: Chosen for A2A protocol support and AWS integration
2. **uv over pip/poetry**: Faster dependency resolution and modern Python tooling
3. **Click + Rich**: Professional CLI experience with beautiful output
4. **Modular architecture**: Separate agents, tools, and configuration for maintainability

### Configuration Strategy
- Environment-based configuration for different deployment scenarios
- Support for multiple LLM providers (Bedrock, OpenAI, Anthropic, etc.)
- Configurable agent behaviors and tool selections

### Testing Strategy
- Unit tests for individual agents and tools
- Integration tests for A2A communication
- End-to-end workflow testing

## 🔍 Usage Examples (Future)

### Basic Multi-Agent Workflow
```python
from multiagent_system.agents import MainAgent, DataAgent, ReportAgent

# Initialize agents
main_agent = MainAgent()
data_agent = DataAgent(port=9001)
report_agent = ReportAgent(port=9002)

# Execute workflow
result = main_agent.process_request("Analyze sales data and generate report")
```

### CLI Usage
```bash
# Run complete workflow
uv run multiagent run --input "data.csv" --output "report.pdf"

# Configure LLM provider
uv run multiagent config --provider bedrock --model claude-3-sonnet

# Monitor agent status
uv run multiagent agents status
```

## 🤝 Contributing

This project follows modern Python development practices:
- Use `uv` for dependency management
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Document all public APIs
- Use type hints throughout

## 📚 Resources

- [Strands Agents Documentation](https://strandsagents.com/)
- [A2A Protocol Specification](https://google-a2a.github.io/A2A/latest/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [uv Documentation](https://docs.astral.sh/uv/)

## 🔮 Future Enhancements

- Web UI for agent monitoring and control
- Integration with vector databases for RAG capabilities
- Support for agent memory and state persistence
- Advanced workflow orchestration patterns
- Performance monitoring and analytics

---

**Note**: This project is in active development. The architecture and implementation details may evolve as we build out the multi-agent functionality.