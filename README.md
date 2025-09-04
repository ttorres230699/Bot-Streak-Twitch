# Installation du bot Twitch sur Windows

## 0. Prérequis

Avant de commencer, assure-toi d’avoir installé :

- **Python** (disponible sur le Microsoft Store)
- **Éditeur de texte** recommandé : [Visual Studio Code](https://code.visualstudio.com/)
- **Bibliothèques Python** :
  - [TwitchIO](https://twitchio.dev/en/latest/) (version 2.2.0)
  - [Pandas](https://pandas.pydata.org/)
  - [asyncio](https://docs.python.org/fr/3.13/library/asyncio.html)

Installe-les avec :

```bash
pip install twitchio==2.2.0 pandas asyncio
```

- **(Optionnel)** [Git](https://git-scm.com/downloads/win) pour faciliter les mises à jour (laisser les options par défaut).

---

## 1. Configuration du bot

### 1.1 Récupération des informations Twitch

1. Va sur [TwitchTokenGenerator](https://twitchtokengenerator.com/), choisis "Bot Chat Twitch" et récupère ton ACCESS TOKEN.
2. Dans le code :
   - Ligne 9 : colle ton ACCESS TOKEN.
   - Ligne 10 : indique le nom de ta chaîne Twitch (sans majuscule).
   - Ligne 12 : règle le temps entre chaque annonce de nouvelle streak (en secondes, par défaut : 60s).
   - Ligne 14 : règle le temps minimal entre deux streams (en heures, par défaut : 12h).
3. Renseigne les récompenses de streak dans le fichier `recompense streak.txt` au format :
   ```
   nb_de_streak_1;recompense_streak_1
   nb_de_streak_2;recompense_streak_2
   ...
   ```

---

## 2. (Optionnel) Lancer le bot en même temps qu’OBS

### 2.1 Modifier le script `obs+bot.bat`

1. Ouvre le fichier `obs+bot.bat` (clic droit > Ouvrir avec > Bloc-notes ou VS Code).
2. Modifie :
   - Ligne 14 : remplace `TonCheminVersLeBot\code` par le chemin du dossier `code`.
   - Ligne 16 : remplace `CheminVersPython\python.exe` par le chemin de l’exécutable Python.
   - Ligne 16 : remplace `CheminVersLeBot\bot.py` par le chemin du fichier `bot.py`.

### 2.2 Créer un raccourci avec l’icône OBS

1. Clic droit sur le fichier `.bat` > Créer un raccourci.
2. Clic droit sur le raccourci > Propriétés.
3. Dans "Cible", mets :
   ```
   C:\Windows\System32\cmd.exe /k "CheminVersLeBat\Obs+bot.bat"
   ```
   Remplace `CheminVersLeBat\Obs+bot.bat` par le chemin réel.
4. Toujours dans Propriétés > "Changer d’icône" > Parcourir :
   ```
   C:\Program Files\obs-studio\bin\64bit\obs64.exe
   ```
5. Glisse le raccourci dans la barre des tâches ou sur le bureau selon tes besoins.


## 3. Mettre à jour le bot avec Git

Si tu viens d’installer Git, voici comment récupérer et mettre à jour le bot :

### 3.1 **Cloner le projet (première utilisation)**  
   Ouvre l’invite de commandes dans le dossier où tu veux installer le bot, puis tape :
   ```bash
   git clone https://github.com/ttorres230699/Bot-Streak-Twitch
   ```

### 3.2 **Mettre à jour le bot (par la suite)**  
   Pour récupérer les dernières modifications, va dans le dossier du bot et tape :
   ```bash
   git pull
   ```

> **Astuce :** Tu peux aussi utiliser [GitHub Desktop](https://desktop.github.com/) pour une interface
---

N’hésite pas à me demander si tu veux encore plus de clarté sur discord : tibz99