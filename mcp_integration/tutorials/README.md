# MCP Integration Tutorials

Interactive tutorials for setting up and using MCP with different AI clients.

## Quick Start

### Option 1: Guided Setup Script
```bash
cd <path-to>/mcp_integration/tutorials
python guided_setup.py
```
This interactive script will:
- Detect your project path
- Set up Python environment
- Generate personalized configurations
- Test the MCP server

### Option 2: Manual Step-by-Step
Follow the detailed tutorials:
- **[Amazon Q Interactive Tutorial](amazon_q_interactive.md)** - Complete walkthrough for Q CLI
- More client tutorials coming soon...

## What You'll Learn

- How to configure MCP servers with AI clients
- Security testing through AI chat interfaces  
- Troubleshooting common MCP issues
- Best practices for MCP tool development

## Generated Configurations

The guided setup script creates personalized config files in `generated_configs/`:
- `amazon_q_setup.sh` - Commands for Q CLI setup
- `vscode_settings.json` - VS Code/Cline configuration
- `claude_config.json` - Claude Desktop configuration

## Prerequisites

- Python 3.8+
- Your chosen AI client (Amazon Q CLI, Cline, or Claude Desktop)
- Basic command line familiarity
