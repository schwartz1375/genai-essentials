#!/usr/bin/env python3
"""
Security MCP Server
AI-powered security testing tools for MCP clients
"""

import subprocess
import json
import socket
import requests
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SecurityToolkit")

@mcp.tool()
def nmap_scan(target: str, scan_type: str = "basic") -> str:
    """Network scanning with nmap
    
    Args:
        target: IP address or hostname to scan
        scan_type: Type of scan (basic, port, service, vuln)
    """
    scan_options = {
        "basic": "-sn",
        "port": "-sS -F", 
        "service": "-sV",
        "vuln": "--script vuln"
    }
    
    cmd = f"nmap {scan_options.get(scan_type, '-sn')} {target}"
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
        return f"Scan Results:\n{result.stdout}"
    except Exception as e:
        return f"Scan failed: {str(e)}"

@mcp.tool()
def port_check(host: str, port: int) -> str:
    """Check if a specific port is open
    
    Args:
        host: Target hostname or IP
        port: Port number to check
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return f"Port {port} on {host}: {'OPEN' if result == 0 else 'CLOSED'}"
    except Exception as e:
        return f"Port check failed: {str(e)}"

@mcp.tool()
def web_headers(url: str) -> str:
    """Analyze HTTP headers for security issues
    
    Args:
        url: Target URL to analyze
    """
    try:
        response = requests.head(url, timeout=10)
        headers = dict(response.headers)
        
        security_headers = {
            'X-Frame-Options': 'Missing - Clickjacking protection',
            'X-Content-Type-Options': 'Missing - MIME sniffing protection', 
            'X-XSS-Protection': 'Missing - XSS protection',
            'Strict-Transport-Security': 'Missing - HTTPS enforcement',
            'Content-Security-Policy': 'Missing - Content injection protection'
        }
        
        analysis = []
        for header, issue in security_headers.items():
            if header not in headers:
                analysis.append(f"⚠️  {issue}")
            else:
                analysis.append(f"✅ {header}: {headers[header]}")
        
        return f"Security Header Analysis for {url}:\n" + "\n".join(analysis)
    except Exception as e:
        return f"Header analysis failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()
