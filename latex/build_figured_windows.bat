@echo off
setlocal

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found in PATH.
  exit /b 1
)

where lualatex >nul 2>nul
if errorlevel 1 (
  echo ERROR: lualatex was not found in PATH.
  exit /b 1
)

python build_figured_version.py
if errorlevel 1 exit /b 1

lualatex -interaction=nonstopmode -halt-on-error generated\main_with_figures.tex
if errorlevel 1 exit /b 1

lualatex -interaction=nonstopmode -halt-on-error generated\main_with_figures.tex
if errorlevel 1 exit /b 1

if not exist main_with_figures.pdf (
  echo ERROR: main_with_figures.pdf was not created.
  exit /b 1
)

echo.
echo SUCCESS: %CD%\main_with_figures.pdf
endlocal
