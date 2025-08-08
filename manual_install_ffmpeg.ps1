# Manual FFmpeg installation script for Windows

# Create a directory for FFmpeg in the user's home directory
$ffmpegDir = "$env:USERPROFILE\ffmpeg"
$ffmpegZip = "$env:TEMP\ffmpeg.zip"
$ffmpegUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

# Create the FFmpeg directory if it doesn't exist
if (-not (Test-Path -Path $ffmpegDir)) {
    New-Item -ItemType Directory -Path $ffmpegDir | Out-Null
    Write-Host "Created FFmpeg directory at: $ffmpegDir"
}

# Download FFmpeg
Write-Host "Downloading FFmpeg from $ffmpegUrl..."
try {
    # Use WebClient for better progress tracking
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($ffmpegUrl, $ffmpegZip)
    Write-Host "FFmpeg downloaded successfully to $ffmpegZip"
} catch {
    Write-Host "Error downloading FFmpeg: $_"
    exit 1
}

# Extract FFmpeg
Write-Host "Extracting FFmpeg to $ffmpegDir..."
try {
    # Create a temporary directory for extraction
    $tempExtractDir = "$env:TEMP\ffmpeg_temp"
    if (Test-Path -Path $tempExtractDir) {
        Remove-Item -Path $tempExtractDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $tempExtractDir | Out-Null
    
    # Extract the zip file
    Expand-Archive -Path $ffmpegZip -DestinationPath $tempExtractDir -Force
    
    # Find the extracted FFmpeg directory (it might be in a subdirectory)
    $extractedDirs = Get-ChildItem -Path $tempExtractDir -Directory
    if ($extractedDirs.Count -eq 0) {
        throw "No directories found in the extracted archive"
    }
    
    # Look for the bin directory
    $sourceBinDir = $null
    foreach ($dir in $extractedDirs) {
        $binPath = Join-Path -Path $dir.FullName -ChildPath "bin"
        if (Test-Path -Path $binPath) {
            $sourceBinDir = $binPath
            break
        }
    }
    
    if (-not $sourceBinDir) {
        throw "Could not find 'bin' directory in the extracted files"
    }
    
    # Copy files to the target directory
    Write-Host "Copying FFmpeg files from $sourceBinDir to $ffmpegDir"
    Copy-Item -Path "$sourceBinDir\*" -Destination $ffmpegDir -Recurse -Force
    
    # Clean up
    Remove-Item -Path $tempExtractDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $ffmpegZip -Force -ErrorAction SilentlyContinue
    
} catch {
    Write-Host "Error extracting FFmpeg: $_"
    exit 1
}

# Add to user PATH if not already present
$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($currentPath -split ';' -notcontains $ffmpegDir) {
    Write-Host "Adding $ffmpegDir to user PATH..."
    [Environment]::SetEnvironmentVariable('Path', "$currentPath;$ffmpegDir", 'User')
    # Also add to current session's PATH for immediate use
    $env:Path = "$env:Path;$ffmpegDir"
}

# Verify installation
Write-Host "`nVerifying FFmpeg installation..."
$ffmpegPath = Join-Path -Path $ffmpegDir -ChildPath "ffmpeg.exe"
if (Test-Path -Path $ffmpegPath) {
    $version = & $ffmpegPath -version | Select-Object -First 1
    Write-Host "FFmpeg installation successful!" -ForegroundColor Green
    Write-Host "Version: $version"
    Write-Host "`nFFmpeg has been installed to: $ffmpegDir"
    Write-Host "This directory has been added to your user PATH."
    Write-Host "You may need to restart your terminal or computer for the PATH changes to take effect."
} else {
    Write-Host "FFmpeg installation verification failed. Please check the installation." -ForegroundColor Red
    exit 1
}

# Instructions for manual PATH update if needed
Write-Host "`nIf FFmpeg is still not recognized, you may need to manually add it to your PATH:"
Write-Host "1. Press Win+R, type 'sysdm.cpl' and press Enter"
Write-Host "2. Go to the 'Advanced' tab and click 'Environment Variables'"
Write-Host "3. Under 'User variables', find and select 'Path', then click 'Edit'"
Write-Host "4. Click 'New' and add: $ffmpegDir"
Write-Host "5. Click 'OK' on all windows to save changes"
