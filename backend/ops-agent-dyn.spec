# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['/home/leiqy/zz-agent/backend'],
    binaries=[],
    datas=[('static', 'static'), ('rag', 'rag'), ('auth.py', '.'), ('db.py', '.'), ('config_loader.py', '.'), ('llm', 'llm'), ('/home/leiqy/zz-agent/backend/venv39/lib/python3.9/site-packages/captcha/data', 'captcha/data')],
    hiddenimports=['pgvector', 'pgvector.sqlalchemy', 'passlib', 'passlib.handlers.bcrypt', 'bcrypt', 'rag', 'rag.retriever', 'rag.loader', 'rag.qa', 'rag.splitter', 'auth', 'db', 'config_loader', 'llm', 'llm.zhipu_client', 'llm.mock_client', 'llm.ollama_client', 'llm.openai_client', 'captcha', 'captcha.image', 'jose', 'jose.jwt', 'openai', 'httpx', 'distro', 'pydantic', 'typing_extensions'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ops-agent-dyn',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
