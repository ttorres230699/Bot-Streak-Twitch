# Installation du bot Twitch sur Windows

## 0. Prérequis

Avant de commencer, assure-toi d’avoir installé :

- [**Python**](https://www.python.org/downloads/   )
- **Éditeur de texte** recommandé : [Visual Studio Code](https://code.visualstudio.com/)
- **Bibliothèques Python** :
  - [TwitchIO](https://twitchio.dev/en/latest/) (version 2.2.0)
  - [Pandas](https://pandas.pydata.org/)
  - [asyncio](https://docs.python.org/fr/3.13/library/asyncio.html)

Installe-les avec :

```bash
pip install twitchio==2.2.0 pandas asyncio
```

-[Git](https://git-scm.com/downloads/win) pour faciliter les mises à jour (laisser les options par défaut).

---

## 1. Configuration du bot

- Dans le dossier où mettre le bot (par exemple Documents, Bureau, etc.) faire un clique droit et sélectionner "Ouvrir le terminal"
- Dans le terminal, coller: 
   ```bash
   git clone https://github.com/ttorres230699/Bot-Streak-Twitch
   ```
- - Ouvre le fichier `.gitignore` et enlève le `#` devant `data/` pour que le dossier `data` ne soit pas suivi par Git.
Le dossier `Bot-Streak-Twitch` est créé avec le code existant
### 1.1 Récupération des informations Twitch

1. Aller sur [TwitchTokenGenerator](https://twitchtokengenerator.com/), choisis "Bot Chat Twitch" et récupère ton ACCESS TOKEN.
2. Dans le dossier data créer le fichier 
   - `recompense streak.txt`
   - `streak viewer.txt`
   - `muted viewer.txt`
   - `date stream.txt`
   - `info chaine.txt` et dedans :
      - À la première ligne mettre le nom de la chaîne sans les majuscules
      - À la deuxième ligne mettre l'ACCES TOKEN
3. Dans le code :
   - Ligne 12 : règle le temps entre chaque annonce de nouvelle streak (en secondes, par défaut : 60s).
   - Ligne 14 : règle le temps minimal entre deux streams (en heures, par défaut : 12h).
4 . Renseigne les récompenses de streak dans le fichier `recompense streak.txt` au format :
   ```
   nb_de_streak_1;recompense_streak_1
   nb_de_streak_2;recompense_streak_2
   ...
   ```

---

## 2. (Optionnel) Lancer le bot en même temps qu’OBS

### 2.1 Modifier le script `obs+bot.bat`

1. Ouvre le fichier `Obs+bot.bat` (clic droit > Ouvrir avec > Bloc-notes ou VS Code).
2. Modifie :
   - Ligne 14 : remplace `TonCheminVersLeBot\code` par le chemin du dossier `code`.
   - Ligne 16 : remplace `CheminVersPython\python.exe` par le chemin de l’exécutable Python.
   - Ligne 16 : remplace `CheminVersLeBot\bot.py` par le chemin du fichier `bot.py`.

### 2.2 Créer un raccourci avec l’icône OBS

1. Clic droit sur le fichier `.bat` > Créer un raccourci.
2. Clic droit sur le raccourci > Propriétés.
3. Dans "Cible", mets :
   ```
   C:\Windows\System32\cmd.exe /k "CheminVersLeBat\obs+bot.bat"
   ```
   Remplace `CheminVersLeBat\Obs+bot.bat` par le chemin réel.
4. Toujours dans Propriétés > "Changer d’icône" > Parcourir :
   ```
   C:\Program Files\obs-studio\bin\64bit\obs64.exe
   ```
5. Glisse le raccourci dans la barre des tâches ou sur le bureau selon tes besoins.


## 3. Mettre à jour le bot avec Git

Pour récupérer les dernières modifications, va dans le dossier du bot et tape :
   ```bash
   git pull
   ```

> **Astuce :** Tu peux aussi utiliser [GitHub Desktop](https://desktop.github.com/) pour une interface
---

N’hésite pas à me demander si tu veux encore plus de clarté sur discord : tibz99