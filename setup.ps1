# Check if Python 3.11 is installed
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3.11") {
    Write-Output "Python 3.11 is installed."

    # Create virtual environment
    python -m venv .venv

    # Activate virtual environment
    .\.venv\Scripts\Activate.ps1

    # Install requirements
    pip install -r requirements.txt
} else {
    Write-Output "Python 3.11 is not installed."
}
