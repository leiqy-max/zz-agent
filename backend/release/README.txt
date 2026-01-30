Ops-Agent for Linux (x86_64) - Static Build
=============================================

This package contains a statically linked binary of the Ops-Agent, 
compatible with older Linux distributions including CentOS 8, RHEL 8, and BCLinux 8.2.

Contents:
- ops-agent: Executable binary (no dependencies required)
- config.yaml: Configuration file template
- init.sql: Database initialization SQL script (RECOMMENDED)
- manual_init_db.py: Database initialization script (optional fallback)
- verify_core.py: Core function verification script (optional)
- verify_llm.py: LLM connection verification script (optional)

Installation:
1. Unzip the package:
   unzip ops-agent-linux-x64.zip
   cd ops-agent

2. Configure:
   Edit config.yaml to set your database and LLM settings.
   (Default LLM: http://10.30.107.200:8000/v1, Model: glm-4)
   (Default DB: localhost:5432)

3. Database Initialization (CRITICAL):
   You MUST ensure the database tables exist before running the agent.
   
   Option A (Recommended): Run the provided `init.sql` script
   Execute the `init.sql` file in your PostgreSQL database using your preferred tool 
   (pgAdmin, DBeaver, or psql). This will create all required tables and the `vector` extension.
   
   Command line example:
   psql -h <host> -U <user> -d <dbname> -f init.sql

   Option B: Manual Python Script
   If you have a Python environment, you can run:
   python manual_init_db.py

   Note: This script creates default users:
   - Admin: admin / admin123
   - User: user / user123

4. Run:
   chmod +x ops-agent
   ./ops-agent

   The service will start on port 9020 (or as configured in config.yaml).

Notes:
- This binary was built using Python 3.9 and staticx to ensure compatibility with glibc 2.28+.
- No external Python or Node.js installation is required for the main binary.
