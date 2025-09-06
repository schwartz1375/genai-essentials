# MCP Integration for AI Security

Model Context Protocol (MCP) enables AI assistants to securely interact with external tools and data sources. This section demonstrates how to build and integrate MCP servers for security testing workflows.

## What is MCP?

MCP is an open protocol developed by Anthropic that standardizes how AI applications communicate with external tools and data sources. It creates a bridge between AI assistants and the broader software ecosystem.

### Core Concepts
- **Servers** - Provide tools, resources, and prompts to AI clients
- **Clients** - AI applications that consume MCP server capabilities  
- **Tools** - Functions that clients can invoke (e.g., file operations, API calls)
- **Resources** - Data sources that clients can read (e.g., files, databases)
- **Prompts** - Reusable prompt templates with arguments

### Why MCP Matters for Security
- **Standardized Tool Integration** - Consistent way to add security tools to AI workflows
- **Controlled Access** - AI assistants can perform security tasks without direct system access
- **Audit Trail** - All tool invocations can be logged and monitored
- **Extensibility** - Custom security tools can be easily integrated

## MCP Security Considerations

### Third-Party Server Risks
**Rug Pull Attacks:**
- Malicious servers can execute arbitrary code with local permissions
- Assume no sandboxing; enforce isolation at deployment (containers, seccomp/AppArmor, read-only FS)
- Dependency on external server availability and trustworthiness

**Tool Overreach:**
- Servers may access more resources than advertised
- Limited fine-grained permission controls
- Difficult to audit actual vs. declared capabilities

**Authentication Gaps:**
- Most MCP servers run without authentication
- Transitive trust issues in production environments
- No standard identity/access management framework

**Supply Chain Compromise:**
- Unsigned/unverified releases or compromised maintainers can ship malicious code
- Typosquatting or lookalike packages/servers
- Unpinned or auto-updating dependencies introduce unexpected changes

**Update Channel & Watering-Hole:**
- Initially benign servers can later ship hostile updates
- Lack of release attestation or provenance tracking

**Data Exfiltration & Telemetry:**
- Prompts, tool args, env vars, and outputs may be logged or transmitted off-host
- Sensitive data may persist in caches or debug dumps

**SSRF & Egress Abuse:**
- Tools can be abused to reach internal services or metadata endpoints
- Unrestricted outbound network access enables scanning or exfiltration

**Sandbox Bypass & Escape:**
- Container/VM misconfig (privileged flags, broad mounts, leaked sockets) enables host access

**DoS, Denial of Wallet & Resource Exhaustion:**
- Unbounded execution time, recursion, or oversized outputs degrade clients or hosts

**Output/Prompt Injection:**
- Server-provided prompts/results can steer the assistant toward unsafe actions
- Schema spoofing or unsafe deserialization of tool outputs

**Manifest Drift & Attestation Gaps:**
- Runtime behavior exceeds declared tools/resources without strong policy enforcement
- No cryptographic attestation of server binary/config at runtime

**Transport Integrity:**
- Missing TLS, weak ciphers, or no certificate pinning
- mTLS not enforced between client and server in production

**Note:** This is not an all-inclusive list of risks. See the [ArtificialDiaries](https://github.com/schwartz1375/ArtificialDiaries) resource for additional guidance on security considerations.

### Security Best Practices
- **Server Allowlisting** - Only use vetted, trusted MCP servers
- **Code Review** - Audit server implementations before deployment
- **Principle of Least Privilege** - Grant minimal necessary permissions
- **Containerization** - Run servers in isolated environments
- **Audit Logging** - Monitor all tool invocations and data access
- **Network Segmentation** - Limit server network access
- **Regular Updates** - Keep servers and dependencies current

## Resources

- **[Official MCP Documentation](https://modelcontextprotocol.io)** - Complete protocol specification and guides
- **[ArtificialDiaries](https://github.com/schwartz1375/ArtificialDiaries)** - Advanced MCP patterns and real-world implementations
- **[MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)** - Open catalog and API for publicly available MCP servers

**Disclaimer:** Third-party MCP servers are listed for convenience only. We make no claims regarding their reliability, security, or suitability for production use. Always review and audit server code before deployment.

## MCP Clients

### Amazon Q CLI
```bash
# Add MCP server
q mcp add --name security-toolkit --command <path-to>/venv/bin/python --args <path-to>/security_mcp.py

# List servers
q mcp list

# Use in chat
q chat
> "Use nmap_scan to check localhost"
```

### Cline (VS Code)
```json
// settings.json
{
  "mcp.servers": {
    "security-toolkit": {
      "command": "<path-to>/venv/bin/python",
      "args": ["<path-to>/security_mcp.py"]
    }
  }
}
```

### Claude Desktop
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "security-toolkit": {
      "command": "<path-to>/venv/bin/python",
      "args": ["<path-to>/security_mcp.py"]
    }
  }
}
```

## Directory Structure

- `configs/` - MCP configuration files for different clients
- `servers/` - Python MCP server implementations
- `demos/` - Example scripts and usage demonstrations
- `tutorials/` - Interactive step-by-step setup guides

## Getting Started

### Quick Start (Recommended)
```bash
cd mcp_integration/tutorials
python guided_setup.py
```
The interactive setup script will guide you through the entire process.

### Manual Setup
1. **Choose Your Tutorial**
   - **[Interactive Tutorials](tutorials/)** - Step-by-step guides with validation
   - **[Configuration Files](configs/)** - Direct setup for experienced users

2. **Setup Environment**
   ```bash
   cd mcp_integration
   python -m venv venv
   source venv/bin/activate 
   pip install -r requirements.txt
   ```

3. **Configure Client** - Follow client-specific setup guides

4. **Test Integration** - Run demos and verify tools work

5. **Build Custom Tools** - Extend the security toolkit

## Security Considerations

### Production Deployment Concerns
When deploying MCP servers in production environments, consider:

**Authentication & Authorization:**
- Implement proper authentication mechanisms
- Use API keys or OAuth for server access
- Consider mutual TLS for client-server communication
- Implement role-based access controls

**Network Security:**
- Deploy servers behind firewalls
- Use VPNs or private networks for sensitive operations
- Implement rate limiting and DDoS protection
- Monitor network traffic for anomalies

**Data Protection:**
- Encrypt sensitive data in transit and at rest
- Implement data retention policies
- Ensure compliance with privacy regulations
- Use secure credential management

**Operational Security:**
- Regular security assessments and penetration testing
- Incident response procedures
- Security monitoring and alerting
- Backup and disaster recovery plans

### Development Security
- Input validation and sanitization
- Secure coding practices
- Dependency vulnerability scanning
- Regular security updates

## Removal/Uninstall

To remove the MCP integration:

### Amazon Q CLI
```bash
# Remove MCP server
q mcp remove --name security-toolkit

# Verify removal
q mcp list
```

### Claude Desktop
Remove the server entry from `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    // Remove the "security-toolkit" entry
  }
}
```

### Cline (VS Code)
Remove the server entry from VS Code `settings.json`:
```json
{
  "mcp.servers": {
    // Remove the "security-toolkit" entry
  }
}
```

### Clean Up Files
```bash
# Remove virtual environment
rm -rf mcp_integration/venv

# Remove generated configs (optional)
rm -rf mcp_integration/generated_configs
```
