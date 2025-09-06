#!/usr/bin/env python3
"""
Guided MCP Setup Script
Interactive setup for MCP integration with personalized configurations
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def get_project_path():
    """Get the project root path from user"""
    print("🔧 MCP Integration Setup")
    print("=" * 40)
    
    current_dir = os.getcwd()
    if "mcp_integration" in current_dir:
        suggested_path = str(Path(current_dir).parent)
    else:
        suggested_path = current_dir
    
    print(f"Current directory: {current_dir}")
    path = input(f"Enter your genai-essentials project path [{suggested_path}]: ").strip()
    
    if not path:
        path = suggested_path
    
    mcp_path = os.path.join(path, "mcp_integration")
    if not os.path.exists(mcp_path):
        print(f"❌ MCP integration directory not found at: {mcp_path}")
        sys.exit(1)
    
    return path

def choose_client():
    """Let user choose MCP client"""
    print("\n📱 Choose your MCP client:")
    print("1. Amazon Q CLI")
    print("2. Cline (VS Code)")
    print("3. Claude Desktop")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return int(choice)
        print("Please enter 1, 2, or 3")

def setup_environment(project_path):
    """Set up Python virtual environment"""
    print("\n🐍 Setting up Python environment...")
    
    mcp_path = os.path.join(project_path, "mcp_integration")
    venv_path = os.path.join(mcp_path, ".venv")
    
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    
    # Install requirements
    pip_path = os.path.join(venv_path, "bin", "pip")
    if os.name == "nt":  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
    
    requirements_path = os.path.join(mcp_path, "requirements.txt")
    print("Installing dependencies...")
    subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
    
    print("✅ Environment setup complete")
    return venv_path

def generate_config(project_path, client_choice, venv_path):
    """Generate personalized configuration"""
    print(f"\n⚙️  Generating configuration...")
    
    python_path = os.path.join(venv_path, "bin", "python")
    server_path = os.path.join(project_path, "mcp_integration", "servers", "security_mcp.py")
    
    if os.name == "nt":  # Windows
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    
    configs = {
        1: {  # Amazon Q
            "type": "q_cli_commands",
            "content": f"""# Amazon Q CLI Setup Commands
q mcp add \\
  --name security-toolkit \\
  --command {python_path} \\
  --args {server_path}

# Verify setup
q mcp list
q mcp status --name security-toolkit"""
        },
        2: {  # Cline
            "type": "vscode_settings",
            "content": {
                "mcp.servers": {
                    "security-toolkit": {
                        "command": python_path,
                        "args": [server_path],
                        "description": "Security testing tools"
                    }
                }
            }
        },
        3: {  # Claude Desktop
            "type": "claude_config",
            "content": {
                "mcpServers": {
                    "security-toolkit": {
                        "command": python_path,
                        "args": [server_path],
                        "description": "Security testing tools"
                    }
                }
            }
        }
    }
    
    config = configs[client_choice]
    
    # Save configuration
    config_dir = os.path.join(project_path, "mcp_integration", "generated_configs")
    os.makedirs(config_dir, exist_ok=True)
    
    if config["type"] == "q_cli_commands":
        config_file = os.path.join(config_dir, "amazon_q_setup.sh")
        with open(config_file, "w") as f:
            f.write(config["content"])
        print(f"✅ Amazon Q setup commands saved to: {config_file}")
        
        # Auto-execute the q mcp add command
        try:
            cmd = ["q", "mcp", "add", "--name", "security-toolkit", "--command", python_path, "--args", server_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MCP server automatically registered with Amazon Q")
            else:
                print(f"⚠️  Auto-registration failed: {result.stderr}")
                print("Run the commands in the setup file manually")
        except Exception as e:
            print(f"⚠️  Auto-registration failed: {e}")
            print("Run the commands in the setup file manually")
    else:
        config_file = os.path.join(config_dir, f"{config['type']}.json")
        with open(config_file, "w") as f:
            json.dump(config["content"], f, indent=2)
        print(f"✅ Configuration saved to: {config_file}")
        
        if client_choice == 2:
            print("Add this configuration to your VS Code settings.json")
        elif client_choice == 3:
            print("Copy this to your Claude Desktop configuration file")

def test_setup(project_path, venv_path):
    """Test the MCP server setup"""
    print(f"\n🧪 Testing MCP server...")
    
    python_path = os.path.join(venv_path, "bin", "python")
    server_path = os.path.join(project_path, "mcp_integration", "servers", "security_mcp.py")
    
    if os.name == "nt":  # Windows
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    
    try:
        # Test server file exists and has required imports
        if not os.path.exists(server_path):
            print(f"⚠️  Server file not found: {server_path}")
            return
            
        with open(server_path, 'r') as f:
            content = f.read()
            if 'from mcp.server.fastmcp import FastMCP' in content and '@mcp.tool()' in content:
                print("✅ MCP server validation passed")
            else:
                print("⚠️  Server file missing required MCP components")
                
    except Exception as e:
        print(f"⚠️  Could not validate server: {e}")

def main():
    try:
        # Get project path
        project_path = get_project_path()
        
        # Choose client
        client_choice = choose_client()
        
        # Setup environment
        venv_path = setup_environment(project_path)
        
        # Generate config
        generate_config(project_path, client_choice, venv_path)
        
        # Test setup
        test_setup(project_path, venv_path)
        
        print(f"\n🎉 Setup complete!")
        print(f"Project path: {project_path}")
        print(f"Next: Follow the generated configuration instructions")
        
    except KeyboardInterrupt:
        print(f"\n❌ Setup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
