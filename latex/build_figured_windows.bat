@echo off
setlocal

where lualatex >nul 2>nul
if errorlevel 1 (
  echo ERROR: lualatex was not found in PATH.
  echo Install TeX Live and reopen this terminal.
  exit /b 1
)

if not exist generated/main_with_figures.tex (
  echo ERROR: generated/main_with_figures.tex is missing.
  echo Run: git switch figure-layout-prototype
  echo      git pull
  exit /b 1
)

if not exist ..\figures\pdf\fig00_knowledge_map.pdf (
  echo ERROR: ..\figures\pdf is missing.
  echo Run: git pull
  exit /b 1
)

lualatex -interaction=nonstopmode -halt-on-error generated/main_with_figures.tex
if errorlevel 1 exit /b 1

lualatex -interaction=nonstopmode -halt-on-error generated/main_with_figures.tex
if errorlevel 1 exit /b 1

if not exist main_with_figures.pdf (
  echo ERROR: main_with_figures.pdf was not created.
  exit /b 1
)

echo.
echo SUCCESS: %CD%\main_with_figures.pdf
endlocal
