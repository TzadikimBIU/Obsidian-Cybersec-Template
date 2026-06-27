# NotebookLM MCP CLI Installation Script for Windows
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "NotebookLM MCP CLI Installation Script (Windows)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check for uv (recommended)
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Found uv (recommended installer)" -ForegroundColor Green
    Write-Host "Installing notebooklm-mcp-cli using uv..."
    uv tool install notebooklm-mcp-cli
    Write-Host "[OK] Installation complete using uv" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  nlm --help"
    Write-Host "  nlm login"
    exit 0
}

# Fallback to pip
if (Get-Command pip -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Found pip (fallback installer)" -ForegroundColor Green
    Write-Host "Installing notebooklm-mcp-cli using pip..."
    pip install notebooklm-mcp-cli
    Write-Host "[OK] Installation complete using pip" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  nlm --help"
    Write-Host "  nlm login"
    exit 0
}

Write-Host "[ERROR] Neither 'uv' nor 'pip' was found in the system path." -ForegroundColor Red
Write-Host "Please install uv (recommended) or Python before proceeding."
exit 1
