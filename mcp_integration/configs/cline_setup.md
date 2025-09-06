# Cline (VS Code) MCP Setup

## Installation

1. Install Cline extension in VS Code
2. Configure MCP servers in VS Code settings

## Configuration

### Method 1: VS Code Settings UI
1. Open VS Code Settings (Cmd+,)
2. Search for "mcp"
3. Add server configuration

### Method 2: settings.json
Add to your VS Code `settings.json`:

```json
{
  "mcp.servers": {
    "security-toolkit": {
      "command": "<path-to>/mcp_integration/venv/bin/python",
      "args": ["<path-to>/mcp_integration/servers/security_mcp.py"],
      "description": "Security testing tools"
    }
  }
}
```

## Usage

1. Open Cline chat panel in VS Code
2. Reference MCP tools in your requests:
   - "Use nmap_scan to check my local network"
   - "Analyze security headers for my website"
   - "Check if port 8080 is open on localhost"

## Troubleshooting

- Ensure Python virtual environment is activated
- Check VS Code developer console for MCP errors
- Verify file paths are absolute and correct
