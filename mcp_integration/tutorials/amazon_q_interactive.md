# Interactive Amazon Q MCP Tutorial

Follow this step-by-step guide to set up and test MCP with Amazon Q CLI.

## Prerequisites Check

**✅ Checkpoint 1: Verify Amazon Q CLI**
```bash
q --version
```
Expected: Version number displayed. If not installed, run the setup script first.

**✅ Checkpoint 2: Check Project Structure**
```bash
ls <path-to>/mcp_integration/
```
Expected: You should see `configs/`, `servers/`, `demos/`, `tutorials/`

## Step 1: Environment Setup

**Create Python Virtual Environment:**
```bash
cd <path-to>/mcp_integration
python -m venv .venv
source .venv/bin/activate  
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**✅ Checkpoint 3: Test MCP Server**
```bash
python servers/security_mcp.py --help
```
Expected: MCP server help message or no errors

## Step 2: Configure Amazon Q

**Add MCP Server:**
```bash
q mcp add \
  --name security-toolkit \
  --command <path-to>/mcp_integration/venv/bin/python \
  --args <path-to>/mcp_integration/servers/security_mcp.py \
  --description "Security testing tools"
```

**✅ Checkpoint 4: Verify Server Added**
```bash
q mcp list
```
Expected: `security-toolkit` appears in the list

**Check Server Status:**
```bash
q mcp status --name security-toolkit
```
Expected: Server shows as running or available

## Step 3: Test MCP Integration

**Start Q CLI Chat:**
```bash
q chat
```

**✅ Checkpoint 5: List Available Tools**
In Q chat, type:
```
/tools
```
Expected: You should see `nmap_scan`, `port_check`, `web_headers`

## Step 4: Interactive Security Testing

**Test 1: Port Check**
```
Check if port 443 is open on google.com using port_check
```
Expected: Response showing port 443 is OPEN

**Test 2: Security Headers**
```
Analyze security headers for https://httpbin.org using web_headers
```
Expected: Analysis of security headers with ✅ and ⚠️ indicators

**Test 3: Network Scan (Safe)**
```
Use nmap_scan to do a basic scan of 127.0.0.1
```
Expected: Nmap output showing localhost is up

## Step 5: Troubleshooting

**If tools don't appear:**
```bash
# Check server logs
q mcp logs --name security-toolkit

# Remove and re-add server
q mcp remove --name security-toolkit
# Then repeat Step 2
```

**If commands fail:**
- Ensure virtual environment is activated
- Check that nmap is installed: `brew install nmap` (macOS)
- Verify Python path is correct in configuration

## ✅ Final Checkpoint

You've successfully:
- ✅ Set up MCP server environment
- ✅ Configured Amazon Q CLI with security toolkit
- ✅ Tested security tools through AI chat interface
- ✅ Performed basic security assessments

**Next Steps:**
- Explore advanced security scenarios
- Build custom MCP tools
- Integrate with CI/CD pipelines
