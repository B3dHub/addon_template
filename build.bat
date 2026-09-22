@echo off
setlocal

REM ====================================
REM Release Build Script
REM Purpose: Clones repository, packages release
REM ====================================

REM --- Set default configuration ---
set branch=dev

REM --- Handle command line arguments ---
REM If branch name is provided as argument, use it
if not "%1"=="" (
    set branch=%1
)

REM --- Create releases directory if it doesn't exist ---
if not exist releases mkdir releases

REM --- Get current project name from directory path ---
for %%I in ("%~dp0.") do set project=%%~nxI

REM --- Remove stale clone from a previous failed run ---
if exist releases\%project% rd /s /q releases\%project%

REM --- Resolve the repository URL from the local origin remote ---
set repo_url=
for /f "delims=" %%u in ('git config --get remote.origin.url') do set repo_url=%%u
if "%repo_url%"=="" (
    echo ERROR: no git "origin" remote found in %CD%
    exit /b 1
)

REM --- Clone repository with specified branch ---
git clone -b %branch% --recurse-submodules "%repo_url%" releases\%project%
cd releases

REM --- Clean up git, github, agents and dev-only files ---
rd /s /q %project%\.git
if exist %project%\.github rd /s /q %project%\.github
if exist %project%\.agents rd /s /q %project%\.agents
if exist %project%\AGENTS.md del /q %project%\AGENTS.md
if exist %project%\.gitmodules del /q %project%\.gitmodules
if exist %project%\build.bat del /q %project%\build.bat
if exist %project%\Makefile del /q %project%\Makefile
if exist %project%\tests rd /s /q %project%\tests
if exist %project%\sync_agents.ps1 del /q %project%\sync_agents.ps1
if exist %project%\.gitignore del /q %project%\.gitignore

REM --- Extract version number from __init__.py ---
for /f "tokens=2-4 delims=(), " %%a in ('findstr /R "version" %project%\__init__.py') do set version=%%a.%%b.%%c
echo Version: %version%

REM --- Create ZIP archive using WinRAR (start /wait: GUI app, cmd does not wait for it) ---
start /wait "" "C:\Program Files\WinRAR\WinRAR.exe" a -afzip -r .\%project%_v%version%.zip .\%project%

REM --- Clean up temporary files ---
rd /s /q %project%

endlocal