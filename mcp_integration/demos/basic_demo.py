#!/usr/bin/env python3
"""
Basic MCP Security Demo
Demonstrates security toolkit functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servers.security_mcp import nmap_scan, port_check, web_headers

def demo_security_tools():
    """Demonstrate security toolkit capabilities"""
    
    print("🔒 Security MCP Toolkit Demo\n")
    
    # Port check demo
    print("1. Port Check Demo:")
    result = port_check("google.com", 443)
    print(f"   {result}\n")
    
    # Web headers demo  
    print("2. Security Headers Demo:")
    result = web_headers("https://httpbin.org")
    print(f"   {result}\n")
    
    # Network scan demo (localhost only for safety)
    print("3. Network Scan Demo:")
    result = nmap_scan("127.0.0.1", "basic")
    print(f"   {result}")

if __name__ == "__main__":
    demo_security_tools()
