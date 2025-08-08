# PowerShell script to download and install FFmpeg on Windows

# Create a directory for FFmpeg
$ffmpegDir = "$env:USERPROFILE\ffmpeg"
$ffmpegZip = "$env:TEMP\ffmpeg.zip"
$ffmpegUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

Write-Host "Downloading FFmpeg..."
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $ffmpegZip

# Extract FFmpeg
Write-Host "Extracting FFmpeg..."
Expand-Archive -Path $ffmpegZip -DestinationPath $env:TEMP\ffmpeg_temp -Force

# Find the bin directory in the extracted files
$extractedDir = Get-ChildItem -Path "$env:TEMP\ffmpeg_temp" -Directory | Select-Object -First 1
$ffmpegBinPath = Join-Path -Path $extractedDir.FullName -ChildPath "bin"

# Create destination directory if it doesn't exist
if (-not (Test-Path -Path $ffmpegDir)) {
    New-Item -ItemType Directory -Path $ffmpegDir | Out-Null
}

# Copy FFmpeg files
Write-Host "Installing FFmpeg to $ffmpegDir"
Copy-Item -Path "$ffmpegBinPath\*" -Destination $ffmpegDir -Recurse -Force

# Add to system PATH
$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($currentPath -split ';' -notcontains $ffmpegDir) {
    [Environment]::SetEnvironmentVariable('Path', "$currentPath;$ffmpegDir", 'User')
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") 
}

# Clean up
Remove-Item -Path $ffmpegZip -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:TEMP\ffmpeg_temp" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "FFmpeg has been installed to $ffmpegDir"
Write-Host "The directory has been added to your user PATH."
Write-Host "Please restart any open command prompts for the changes to take effect."

# Verify installation
try {
    $ffmpegVersion = & "$ffmpegDir\ffmpeg.exe" -version | Select-Object -First 1
    Write-Host "FFmpeg version: $ffmpegVersion"
} catch {
    Write-Host "FFmpeg installation verification failed. Please check the installation."
}
