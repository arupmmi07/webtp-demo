#!/usr/bin/env python3
"""
Verify that the project is ready for Render.com deployment.

This script checks:
- Required files exist
- Dependencies are correct
- Configuration is valid
- Data files are present
"""

import os
import sys
from pathlib import Path
import json

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def check_file(filepath, required=True):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"{Colors.GREEN}✓{Colors.END} {filepath}")
        return True
    else:
        status = "REQUIRED" if required else "OPTIONAL"
        color = Colors.RED if required else Colors.YELLOW
        print(f"{color}✗{Colors.END} {filepath} ({status})")
        return not required

def check_requirements():
    """Check if requirements.txt has necessary dependencies."""
    print_header("📦 Checking Dependencies")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'streamlit',
        'litellm',
        'langfuse',
        'langgraph',
        'pyyaml',
        'python-dotenv'
    ]
    
    all_good = True
    
    if not Path('requirements.txt').exists():
        print(f"{Colors.RED}✗ requirements.txt not found!{Colors.END}")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read().lower()
    
    for package in required_packages:
        if package in content:
            print(f"{Colors.GREEN}✓{Colors.END} {package} found")
        else:
            print(f"{Colors.RED}✗{Colors.END} {package} missing")
            all_good = False
    
    return all_good

def check_render_files():
    """Check if Render deployment files exist."""
    print_header("🚀 Checking Render Files")
    
    files = {
        'render.yaml': True,
        'render_start.sh': True,
        'render_start_ui.sh': True,
        '.renderignore': False,
        'RENDER_QUICK_START.md': False,
        'RENDER_DEPLOYMENT.md': False,
        'env.render.example': False,
    }
    
    all_good = True
    for filepath, required in files.items():
        if not check_file(filepath, required):
            if required:
                all_good = False
    
    return all_good

def check_api_server():
    """Check if API server file is valid."""
    print_header("🔧 Checking API Server")
    
    api_file = Path('api/server.py')
    if not api_file.exists():
        print(f"{Colors.RED}✗ api/server.py not found!{Colors.END}")
        return False
    
    print(f"{Colors.GREEN}✓{Colors.END} api/server.py exists")
    
    # Check if FastAPI app is defined
    with open(api_file, 'r') as f:
        content = f.read()
        
    checks = {
        'FastAPI app': 'app = FastAPI(' in content,
        'Health endpoint': '/health' in content,
        'CORS middleware': 'CORSMiddleware' in content or 'add_middleware' in content,
        'Uvicorn ready': '__name__' in content and 'uvicorn' in content,
    }
    
    all_good = True
    for check_name, passed in checks.items():
        if passed:
            print(f"{Colors.GREEN}✓{Colors.END} {check_name}")
        else:
            print(f"{Colors.YELLOW}⚠{Colors.END} {check_name} (may need verification)")
    
    return all_good

def check_streamlit_ui():
    """Check if Streamlit UI is ready."""
    print_header("🎨 Checking Streamlit UI")
    
    ui_file = Path('demo/chat_ui.py')
    if not ui_file.exists():
        print(f"{Colors.RED}✗ demo/chat_ui.py not found!{Colors.END}")
        return False
    
    print(f"{Colors.GREEN}✓{Colors.END} demo/chat_ui.py exists")
    return True

def check_data_files():
    """Check if data files exist."""
    print_header("📊 Checking Data Files")
    
    data_dir = Path('data')
    if not data_dir.exists():
        print(f"{Colors.RED}✗ data/ directory not found!{Colors.END}")
        return False
    
    files = [
        'appointments.json',
        'patients.json',
        'providers.json',
        'waitlist.json',
        'freed_slots.json',
        'emails.json'
    ]
    
    all_good = True
    for filename in files:
        filepath = data_dir / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    json.load(f)
                print(f"{Colors.GREEN}✓{Colors.END} {filename} (valid JSON)")
            except json.JSONDecodeError:
                print(f"{Colors.YELLOW}⚠{Colors.END} {filename} (invalid JSON, will be reset)")
        else:
            print(f"{Colors.YELLOW}⚠{Colors.END} {filename} (will be created on deploy)")
    
    # Check backups
    backup_dir = data_dir / 'backups'
    if backup_dir.exists():
        print(f"{Colors.GREEN}✓{Colors.END} data/backups/ exists")
    else:
        print(f"{Colors.YELLOW}⚠{Colors.END} data/backups/ missing (optional)")
    
    return all_good

def check_render_yaml():
    """Validate render.yaml configuration."""
    print_header("📝 Validating render.yaml")
    
    yaml_file = Path('render.yaml')
    if not yaml_file.exists():
        print(f"{Colors.RED}✗ render.yaml not found!{Colors.END}")
        return False
    
    with open(yaml_file, 'r') as f:
        content = f.read()
    
    checks = {
        'API service': 'name: webtp-api' in content,
        'UI service': 'name: webtp-ui' in content,
        'Database': 'databases:' in content,
        'Python env': 'env: python' in content,
        'Build command': 'buildCommand:' in content,
        'Start command': 'startCommand:' in content,
        'Health check': 'healthCheckPath:' in content,
        'Environment vars': 'envVars:' in content,
    }
    
    all_good = True
    for check_name, passed in checks.items():
        if passed:
            print(f"{Colors.GREEN}✓{Colors.END} {check_name}")
        else:
            print(f"{Colors.RED}✗{Colors.END} {check_name}")
            all_good = False
    
    return all_good

def check_git():
    """Check if git repository is ready."""
    print_header("📦 Checking Git Repository")
    
    if not Path('.git').exists():
        print(f"{Colors.YELLOW}⚠{Colors.END} Not a git repository (run 'git init')")
        return False
    
    print(f"{Colors.GREEN}✓{Colors.END} Git repository initialized")
    
    # Check if there are uncommitted changes
    import subprocess
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print(f"{Colors.YELLOW}⚠{Colors.END} Uncommitted changes detected")
            print(f"  Run: git add . && git commit -m 'Ready for Render'")
        else:
            print(f"{Colors.GREEN}✓{Colors.END} No uncommitted changes")
    except:
        print(f"{Colors.YELLOW}⚠{Colors.END} Could not check git status")
    
    return True

def main():
    """Run all checks."""
    os.chdir(Path(__file__).parent)
    
    print(f"\n{Colors.BOLD}🔍 Verifying Render.com Deployment Readiness{Colors.END}")
    print(f"{Colors.BOLD}Project: Healthcare Operations Assistant{Colors.END}")
    
    checks = [
        ("Requirements", check_requirements),
        ("Render Files", check_render_files),
        ("API Server", check_api_server),
        ("Streamlit UI", check_streamlit_ui),
        ("Data Files", check_data_files),
        ("Render YAML", check_render_yaml),
        ("Git Repository", check_git),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"{Colors.RED}✗ Error checking {name}: {e}{Colors.END}")
            results.append(False)
    
    # Summary
    print_header("📊 Summary")
    
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed! ({passed}/{total}){Colors.END}")
        print(f"\n{Colors.GREEN}🚀 Ready to deploy to Render.com!{Colors.END}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.END}")
        print(f"1. git add . && git commit -m 'Ready for Render'")
        print(f"2. git push origin main")
        print(f"3. Go to https://dashboard.render.com")
        print(f"4. Click 'New +' → 'Blueprint'")
        print(f"5. Select your repository")
        print(f"\n{Colors.BLUE}📖 See RENDER_QUICK_START.md for detailed instructions{Colors.END}")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ Some checks failed ({passed}/{total} passed){Colors.END}")
        print(f"\n{Colors.YELLOW}Fix the issues above before deploying.{Colors.END}")
        print(f"{Colors.BLUE}📖 See RENDER_DEPLOYMENT.md for troubleshooting{Colors.END}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

