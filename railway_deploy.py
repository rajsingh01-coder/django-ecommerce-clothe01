#!/usr/bin/env python
"""
Railway Deployment Preparation Script
This script prepares the Django project for Railway deployment
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_git_status():
    """Check if git repository is ready"""
    print("\n📋 Checking Git status...")
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("❌ Git repository not found. Initializing...")
        if not run_command("git init", "Initializing Git repository"):
            return False
    
    # Check if files are staged
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Files need to be committed")
        return False
    else:
        print("✅ Git repository is clean")
        return True

def prepare_for_deployment():
    """Prepare project for Railway deployment"""
    print("\n🚀 Preparing for Railway Deployment...")
    
    # 1. Check git status
    if not check_git_status():
        print("\n📝 Staging files for commit...")
        if not run_command("git add .", "Adding files to git"):
            return False
        
        if not run_command('git commit -m "Prepare for Railway deployment"', "Committing changes"):
            return False
    
    # 2. Check if remote exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" not in result.stdout:
        print("\n⚠️  No remote repository found.")
        print("Please create a GitHub repository and add it as origin:")
        print("git remote add origin https://github.com/yourusername/your-repo-name.git")
        return False
    
    # 3. Push to GitHub
    print("\n📤 Pushing to GitHub...")
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        return False
    
    print("\n🎉 Project is ready for Railway deployment!")
    return True

def show_deployment_instructions():
    """Show Railway deployment instructions"""
    print("\n" + "="*60)
    print("🚀 RAILWAY DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    print("\n📋 Step-by-Step Guide:")
    print("1. Go to https://railway.app")
    print("2. Sign up/Login with GitHub")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose your repository")
    print("6. Railway will automatically detect Django")
    
    print("\n🔧 Environment Variables to Add:")
    print("SECRET_KEY=your-super-secret-key-here")
    print("DEBUG=False")
    print("EMAIL_HOST_USER=singhraj23036@gmail.com")
    print("EMAIL_HOST_PASSWORD=23037")
    print("ADMIN_EMAIL=singhraj23036@gmail.com")
    
    print("\n🗄️ Database:")
    print("1. In Railway project, click 'New'")
    print("2. Select 'Database' → 'PostgreSQL'")
    print("3. Railway will automatically connect it")
    
    print("\n⏱️  Deployment Time: 5-10 minutes")
    print("\n🎉 Your website will be live at: https://your-app-name.railway.app")

def main():
    """Main function"""
    print("🚀 Railway Deployment Preparation")
    print("="*50)
    
    if prepare_for_deployment():
        show_deployment_instructions()
    else:
        print("\n❌ Deployment preparation failed!")
        print("Please fix the issues and try again.")

if __name__ == "__main__":
    main() 