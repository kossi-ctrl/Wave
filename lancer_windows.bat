@echo off
title Wave - Lancement

echo.
echo  ==================================
echo        Lancement de Wave
echo  ==================================
echo.

:: Vérifier que Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERREUR] Python n'est pas installe.
    echo.
    echo  Suis le guide INSTALLER_PYTHON.md pour l'installer,
    echo  puis relance ce fichier.
    echo.
    pause
    exit /b 1
)

:: Aller dans le bon dossier
cd /d "%~dp0"

:: Créer le fichier .env si absent
if not exist ".env" (
    copy ".env.docker" ".env" >nul
)

:: Créer le venv si absent
if not exist "venv\" (
    echo  Creation de l'environnement Python...
    python -m venv venv
)

:: Activer le venv
call venv\Scripts\activate.bat

:: Installer les dépendances
echo  Installation des dependances...
pip install -r requirements.txt --quiet

:: Migrations
echo  Preparation de la base de donnees...
python manage.py migrate --noinput

:: Charger les données
python manage.py loaddata wave_data_fixed.json 2>nul

:: Fichiers statiques
python manage.py collectstatic --noinput --quiet

:: Ouvrir le navigateur après 2 secondes
echo.
echo  ==================================
echo   Wave est pret !
echo   Ouverture de http://localhost:8000
echo  ==================================
echo.
start "" timeout /t 2 >nul
start http://localhost:8000

:: Lancer le serveur
python manage.py runserver

pause
