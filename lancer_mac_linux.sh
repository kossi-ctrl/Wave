#!/bin/bash

echo ""
echo " =================================="
echo "       Lancement de Wave"
echo " =================================="
echo ""

# Aller dans le dossier du script
cd "$(dirname "$0")"

# Vérifier que Python est installé
if ! command -v python3 &>/dev/null; then
    echo " [ERREUR] Python n'est pas installé."
    echo ""
    echo " Suis le guide INSTALLER_PYTHON.md pour l'installer,"
    echo " puis relance ce fichier."
    echo ""
    read -p "Appuie sur Entrée pour fermer..."
    exit 1
fi

# Créer le .env si absent
if [ ! -f ".env" ]; then
    cp .env.docker .env
fi

# Créer le venv si absent
if [ ! -d "venv" ]; then
    echo " Création de l'environnement Python..."
    python3 -m venv venv
fi

# Activer le venv
source venv/bin/activate

# Installer les dépendances
echo " Installation des dépendances..."
pip install -r requirements.txt --quiet

# Migrations
echo " Préparation de la base de données..."
python manage.py migrate --noinput

# Charger les données
python manage.py loaddata wave_data_fixed.json 2>/dev/null

# Fichiers statiques
python manage.py collectstatic --noinput --quiet

echo ""
echo " =================================="
echo "  Wave est prêt !"
echo "  Ouverture de http://localhost:8000"
echo " =================================="
echo ""

# Ouvrir le navigateur
sleep 2
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
else
    xdg-open http://localhost:8000 2>/dev/null
fi

# Lancer le serveur
python manage.py runserver
