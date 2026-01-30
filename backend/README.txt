Ops-Agent for Linux (x86_64) - Static Build
=============================================

This package contains a statically linked binary of the Ops-Agent, 
compatible with older Linux distributions including CentOS 8, RHEL 8, and BCLinux 8.2.

Contents:
- ops-agent: Executable binary (no dependencies required)
- config.yaml: Configuration file template
- manual_init_db.py: Database initialization script (optional fallback)
- verify_core.py: Core function verification script (optional)

Installation:
1. Unzip the package:
   unzip ops-agent-linux-x64.zip
   cd ops-agent

2. Configure:
   Edit config.yaml to set your database and LLM settings.
   (Default LLM: http://10.30.107.200:8000/v1, Model: glm-4)
   (Default DB: localhost:5432)

3. Database Initialization:
   The `ops-agent` binary will automatically attempt to create necessary tables on startup.
   
   If you encounter database errors (e.g. "UndefinedTable"), it means automatic initialization failed.
   You can try running the manual initialization script if you have a Python environment:
   
   pip install sqlalchemy psycopg2-binary pyyaml python-dotenv passlib bcrypt
   python manual_init_db.py
   
   Note: If pgvector extension creation fails (due to permissions), the agent will still work
   for Login/Register/Chat, but RAG (Document Search) features will be disabled.

4. Run:
   chmod +x ops-agent
   ./ops-agent

   The service will start on port 9020 (or as configured in config.yaml).

Notes:
- This binary was built using Python 3.9 and staticx to ensure compatibility with glibc 2.28+.
- No external Python or Node.js installation is required for the main binary.
