$BASE_DIR = $PSScriptRoot
$VENV_DIR = Join-Path $BASE_DIR '.venv'
$ACTIVATE_VENV = Join-Path $VENV_DIR 'Scripts/Activate.ps1'

if (-not (Test-Path -PathType Container -Path $VENV_DIR)) {
    Write-Host "Venv does not exist, creating"
    python -m venv $VENV_DIR
}

. ($ACTIVATE_VENV)

python -m pip install --upgrade pip
python -m pip install wheel
python -m pip install -r requirements.txt

# Upgrade all
# python -m pip freeze | %{$_.split('==')[0]} | %{python -m pip install --upgrade $_}
# python -m pip freeze > requirements.txt
