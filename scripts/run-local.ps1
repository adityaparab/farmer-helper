param(
    [string]$PythonPath = "./.venv/Scripts/python.exe"
)

if (-not (Test-Path $PythonPath)) {
    throw "Python executable not found at $PythonPath. Create and activate .venv first."
}

& $PythonPath -m pip install -e .[dev]
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

& $PythonPath -m alembic upgrade head
if ($LASTEXITCODE -ne 0) {
    throw "Migration failed."
}

& $PythonPath -m uvicorn farmer_helper.main:app --reload --host 127.0.0.1 --port 8000
