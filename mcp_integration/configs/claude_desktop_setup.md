# Claude Desktop MCP Setup

## Installation

1. Download Claude Desktop from Anthropic
2. Install and launch the application

## Configuration

### Configuration File Location
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Setup Steps

1. **Create/Edit Configuration File**
```json
{
  "mcpServers": {
    "security-toolkit": {
      "command": "<path-to>/mcp_integration/venv/bin/python",
      "args": ["<path-to>/mcp_integration/servers/security_mcp.py"],
      "description": "Security testing tools"
    }
  }
}
```

2. **Restart Claude Desktop**
   - Quit and relaunch the application
   - MCP servers load on startup

## Usage

1. Start a new conversation in Claude Desktop
2. Ask Claude to use the security tools:
   - "Use nmap_scan to check localhost for open ports"
   - "Check if port 443 is open on google.com using port_check"
   - "Analyze security headers for https://example.com with web_headers"

## Verification

Claude will show available MCP tools in the conversation. You should see:
- `nmap_scan` - Network scanning capabilities
- `port_check` - Port connectivity testing  
- `web_headers` - HTTP security header analysis

## Troubleshooting

- Ensure Python virtual environment exists and has required packages
- Check file paths are absolute and correct
- Restart Claude Desktop after configuration changes
- Check system console for MCP server errors
