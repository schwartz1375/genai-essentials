# Amazon Q CLI MCP Setup

## Installation


### Install [Amazon Q CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html) (if not already installed)

## Adding MCP Servers

### Method 1: Command Line
```bash
# Add security toolkit server
q mcp add \
  --name security-toolkit \
  --command <path-to>/mcp_integration/venv/bin/python \
  --args <path-to>/mcp_integration/servers/security_mcp.py

# Verify server was added
q mcp list

# Check server status
q mcp status --name security-toolkit
```

### Method 2: Direct Configuration
Edit `~/.aws/amazonq/mcp.json`:

```json
{
  "mcpServers": {
    "security-toolkit": {
      "command": "<path-to>/mcp_integration/venv/bin/python",
      "args": ["<path-to>/mcp_integration/servers/security_mcp.py"]
    }
  }
}
```

## Usage

```bash
# Start Q CLI chat
q chat

# List available tools
/tools

# Use security tools
> "Scan localhost for open ports using nmap_scan"
> "Check if port 22 is open on 192.168.1.1"
> "Analyze security headers for https://example.com"
```

## Troubleshooting

```bash
# Check MCP server logs
q mcp logs --name security-toolkit

# Remove problematic server
q mcp remove --name security-toolkit

# Restart Q CLI if needed
q chat --reset
```
