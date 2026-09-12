$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot
$env:PYTHONPATH = $ProjectRoot
Write-Host "--- ERP Producción Textil ---" -ForegroundColor Green
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"
Write-Host "Aplicando migraciones..." -ForegroundColor Magenta
python manage.py migrate
Write-Host "Iniciando servidor..." -ForegroundColor Yellow
python manage.py runserver