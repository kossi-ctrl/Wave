# Installer Python

## Windows

1. Va sur [python.org/downloads](https://www.python.org/downloads/)
2. Clique sur **"Download Python 3.x.x"** (le gros bouton jaune)
3. Lance le fichier téléchargé
4. ⚠️ **Important** : coche la case **"Add Python to PATH"** en bas avant de cliquer sur Install

   ![Add to PATH](https://www.python.org/static/img/python-logo.png)

5. Clique sur **"Install Now"**
6. Une fois terminé, ferme et rouvre ton terminal

**Vérifier que ça marche** — ouvre le terminal (`cmd`) et tape :
```
python --version
```
Tu dois voir quelque chose comme `Python 3.11.x`.

---

## Mac

Mac vient avec une vieille version de Python. Il faut en installer une récente.

1. Va sur [python.org/downloads](https://www.python.org/downloads/)
2. Clique sur **"Download Python 3.x.x"**
3. Lance le fichier `.pkg` téléchargé
4. Suis les étapes d'installation (tout par défaut)

**Vérifier que ça marche** — ouvre le Terminal et tape :
```
python3 --version
```
Tu dois voir quelque chose comme `Python 3.11.x`.

---

## Linux (Ubuntu / Debian)

Python est généralement déjà installé. Vérifie avec :
```bash
python3 --version
```

Si ce n'est pas le cas :
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

---

## Une fois Python installé

Retourne dans le dossier du projet et :

- **Windows** : double-clique sur `lancer_windows.bat`
- **Mac/Linux** : ouvre le terminal dans le dossier et lance :
  ```bash
  chmod +x lancer_mac_linux.sh && ./lancer_mac_linux.sh
  ```
