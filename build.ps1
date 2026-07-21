$ErrorActionPreference = 'Stop'

$entryScript = 'virtual taylor frame.py'
$appName = 'virtual taylor frame'
$dataFiles = @('empty.wav', 'content.wav', 'move.wav')

function Get-PythonCommand {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return 'python'
    }
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return 'py'
    }
    throw 'Python was not found in PATH.'
}

function Invoke-Build {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$BuildArgs
    )

    if (-not (Test-Path $entryScript)) {
        throw "Entry script not found: $entryScript"
    }

    $pythonCmd = Get-PythonCommand

    $baseArgs = @('-m', 'PyInstaller', '--noconfirm', '--clean', '--name', $appName)

    foreach ($file in $dataFiles) {
        if (Test-Path $file) {
            $baseArgs += @('--add-data', "$file;.")
        } else {
            Write-Warning "Data file missing and will not be bundled: $file"
        }
    }

    $args = $baseArgs + $BuildArgs + @($entryScript)

    Write-Host "Running: $pythonCmd $($args -join ' ')"
    & $pythonCmd @args

    if ($LASTEXITCODE -ne 0) {
        throw "Build failed with exit code $LASTEXITCODE"
    }

    Write-Host ''
    Write-Host 'Build completed successfully.'
    Write-Host "Output: .\\dist"
}

Write-Host 'Select build type:'
Write-Host '1. Single executable (no console)'
Write-Host '2. Debug executable'
Write-Host '3. Folder-based build'

$choice = Read-Host 'Enter option number (1-3)'

switch ($choice) {
    '1' {
        Invoke-Build -BuildArgs @('--onefile', '--windowed')
    }
    '2' {
        Invoke-Build -BuildArgs @('--onefile', '--console', '--debug', 'all')
    }
    '3' {
        Invoke-Build -BuildArgs @('--onedir', '--windowed')
    }
    default {
        Write-Error 'Invalid selection. Please run the script again and choose 1, 2, or 3.'
        exit 1
    }
}
