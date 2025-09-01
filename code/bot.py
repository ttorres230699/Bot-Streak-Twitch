from twitchio.ext import commands #twitchio 2.2.0
import pandas as pd
import asyncio

# Configuration de l'API Twitch
# Remplacez les valeurs par vos propres identifiants
#my_client_id = "" # https://dev.twitch.tv/console
#my_client_secret_id = "" # https://dev.twitch.tv/console
my_oauth_token = "" # https://twitchtokengenerator.com/
my_channel = ""  # Remplacez par le nom de votre chaîne

temps_boucle_annonce = 60 # Temps d'attente entre chaque annonce en secondes

ecart_min_stream = 12 # Ecart minimum entre deux streams en heures

#récupération de l'ID du bot

#headers = {
#    "Client-ID": my_client_id,
#    "Authorization": f"Bearer {my_oauth_token}"
#}
#
#response = requests.get("https://api.twitch.tv/helix/users", headers=headers)
#data = response.json()
#print(data)
#my_bot_id = data['data'][0]['id']

# Chargement des données depuis les fichiers texte

recompense_streak = pd.read_csv("../data/recompense streak.txt", header=None, names=["Streak", "Récompense"], sep=";",dtype={"Streak": int, "Récompense": str})

# Trier les récompenses par ordre croissant de streak

streak_viewer = pd.read_csv("../data/streak viewer.txt", header=0, names=["Id","Viewer", "Streak","Derniere Date de Connexion"], sep=";",dtype={ "Viewer": str, "Streak": int}, parse_dates=["Derniere Date de Connexion"])

annonce_streak = pd.DataFrame(columns=["Viewer", "Streak"])



# Vérification de la date du dernier stream

date_stream =  pd.Timestamp.now()

with open("../data/date stream.txt","a+",encoding="utf-8") as f:
    f.seek(0)  # Rewind the file to the beginning
    lines = f.readlines()
    if lines:
        der_date_stream = pd.to_datetime(lines[-1].strip())        
    else:
        der_date_stream = None
    if der_date_stream is None or (date_stream - der_date_stream) >= pd.Timedelta(hours=ecart_min_stream):
        f.write(f"{date_stream}\n")
        
    #verifier que le fichier contient au moins deux dates
    elif len(lines) >= 2:
        date_stream = der_date_stream
        der_date_stream = pd.to_datetime(lines[-2].strip())
    else:
        date_stream = der_date_stream
        der_date_stream = None

        
with open("../data/muted viewers.txt","r",encoding="utf-8") as f2:
    muted_viewers = set()
    for line in f2:
        muted_viewers.add(line.strip())
    
    
print(f"Date du dernier stream: {der_date_stream}")
print(f"Date du stream actuel: {date_stream}")  

def prochaine_recompense(id):
    """
    Retourne sa streak et la prochaine récompense pour le viewer en fonction de sa série de visionnage.
    """

    streak = streak_viewer.loc[streak_viewer["Id"] == id, "Streak"].values[0]
    val_exacte=-1
    for val in recompense_streak["Streak"].values:
        if val > streak:
            return val_exacte,val,recompense_streak.loc[recompense_streak["Streak"] == val, "Récompense"].values[0]
        if val == streak:
            val_exacte = val


class MyBot(commands.Bot):

    def __init__(self): 
        super().__init__(
            token="oauth:nrivp7kxtt489df5jyumr2m9w72ck7",
            #client_id=my_client_id, 
            #client_secret=my_client_secret_id,
            #bot_id=my_bot_id,
            prefix='!',
            initial_channels=[my_channel]
        )
        self.liste_pseudo = set()  # Pour éviter les doublons dans les annonces de streaks
        self.liste_recompense = set()
        
    async def event_ready(self):
        print(f'Connecté en tant que {self.nick}')
        self.loop.create_task(self.announce_streak())
        global muted_viewers
        if muted_viewers== set():
            muted_viewers.add(self.nick)
            muted_viewers.add("wizebot")
            muted_viewers.add("streamelements")
            muted_viewers.add("moobot")
            muted_viewers.add("nightbot")    
            with open("../data/muted viewers.txt","w",encoding="utf-8") as f2:
                f2.write(f"{self.nick}\n")
        
    


    async def announce_streak(self):
        await self.wait_for_ready()
        channel = self.get_channel(my_channel)
        await channel.send("Bot de streaks de visionnage v6 prêt !")

        while True:
            print("test")
            await asyncio.sleep(temps_boucle_annonce)

            global annonce_streak
            message = "Voici les streaks des viewers :"
            for index, row in annonce_streak.iterrows():
                viewer = row['Viewer']
                streak = row['Streak']
                if viewer not in muted_viewers and viewer not in self.liste_pseudo:
                    message += f" @{viewer} -> {streak}|"
                    self.liste_pseudo.add(viewer)

            message += " Pour plus d'informations, tapez !botstreak"
            
            channel = self.get_channel(my_channel)
            if message!="Voici les streaks des viewers : Pour plus d'informations, tapez !botstreak":
                await channel.send(message)
            annonce_streak = pd.DataFrame(columns=["Viewer", "Streak"])
        
    @commands.command(name="mystreak") #commande !mystreak
    async def mystreak(self, ctx, username: str = None): 
        global streak_viewer
    # Si aucun pseudo donné, on prend celui de la personne qui appelle la commande
        if not username:
            username = ctx.author.name
        else:
        # Enlève le @ si présent
            username = username.lstrip("@")
        id=streak_viewer.loc[streak_viewer["Viewer"]==username,"Id"].values[0]
        val_exacte,proch_streak,proch_recompense = prochaine_recompense(id)
        if id not in streak_viewer["Id"].values:
            await ctx.send(f"@{username}, tu n'as pas encore commencé ta série de visionnage.")
            return
        elif val_exacte == -1:
            await ctx.send(f"@{username}, tu es a {streak_viewer.loc[streak_viewer['Viewer'] == username, 'Streak'].values[0]} visionnages consécutifs! Prochain objectif : {proch_streak} -> {proch_recompense}.")
        else:
            await ctx.send(f"@{username}, tu es a {streak_viewer.loc[streak_viewer['Viewer'] == username, 'Streak'].values[0]} visionnages consécutifs! Tu peux {recompense_streak.loc[recompense_streak['Streak'] == val_exacte, 'Récompense'].values[0]}. Prochain objectif : {proch_streak} -> {proch_recompense}.")


    @commands.command(name="mutestreak") #commande !mutestreak
    async def mutestreak(self, ctx):
        """
        Commande pour muter le bot de streaks.
        """
        global muted_viewers
        if ctx.author.name not in muted_viewers:
            muted_viewers.add(ctx.author.name)
            with open("../data/muted viewers.txt","a",encoding="utf-8") as f2:
                f2.write(f"{ctx.author.name}\n")
            await ctx.send(f"@{ctx.author.name}, tu as été muté pour les annonces de streaks.")
        else:
            await ctx.send(f"@{ctx.author.name}, tu es déjà muté pour les annonces de streaks.")
            
    @commands.command(name="unmutestreak") #commande !unmutestreak
    async def unmutestreak(self, ctx):
        """
        Commande pour unmuter le bot de streaks.
        """
        global muted_viewers
        if ctx.author.name in muted_viewers:
            muted_viewers.remove(ctx.author.name)
            with open("../data/muted viewers.txt","w",encoding="utf-8") as f2:
                for viewer in muted_viewers:
                    f2.write(f"{viewer}\n")
            await ctx.send(f"@{ctx.author.name}, tu as été unmuté pour les annonces de streaks.")
        else:
            await ctx.send(f"@{ctx.author.name}, tu n'es pas muté pour les annonces de streaks.")
            
    @commands.command(name="botstreak") #commande !botstreak
    async def botstreak(self, ctx):
        """
        Décris les commandes du bot de streaks.
        """
        message = (
            "Voici les commandes du bot de streaks :\n"
            "!mystreak : Affiche ta série de visionnage.\n"
            "!mutestreak : Muter le bot de streaks pour ne plus recevoir d'annonces.\n"
            "!unmutestreak : Unmuter le bot de streaks pour recevoir à nouveau les annonces.\n"
            "!botstreak : Affiche les commandes du bot de streaks.\n"
            "!recompensestreak : Affiche les récompenses disponibles pour les streaks.\n"
            f"Le bot annonce les streaks toutes les {temps_boucle_annonce} secondes."
        )
        await ctx.send(message)
        
@commands.command(name="recompensestreak")  #commande !recompensestreak
async def recompensestreak(self, ctx):
    """
    Affiche les récompenses disponibles pour les streaks.
    """
    message = "Voici les récompenses disponibles pour les streaks :\n"
    for index, row in recompense_streak.iterrows():
        line = f"{row['Streak']} visionnages consécutifs : {row['Récompense']}\n"
        if len(message) + len(line) > 450:
            await ctx.send(message)
            message = ""
        message += line
    if message:
        await ctx.send(message)
     
    
        
    async def event_message(self, message): 
        global streak_viewer, date_stream, der_date_stream,annonce_streak
        print(f"Message reçu de {message.author.name}: {message.content}")
        if message.echo:
            return
        
        if message.author.name in streak_viewer["Viewer"].values and pd.isna(streak_viewer.loc[streak_viewer["Viewer"]==message.author.name, "Id"].values[0]) :
            streak_viewer.loc[streak_viewer["Viewer"]==message.author.name, "Id"].values[0]=message.author.id
        
        if not(message.author.id in streak_viewer["Id"].values):
            new_entry = {
                "Id": message.author.id,
                "Viewer": message.author.name,
                "Streak": 1,
                "Derniere Date de Connexion": date_stream
            }
            streak_viewer=pd.concat([streak_viewer, pd.DataFrame([new_entry])], ignore_index=True)
        elif streak_viewer.loc[streak_viewer["Id"] == message.author.id, "Derniere Date de Connexion"].values[0]== der_date_stream:
            streak_viewer.loc[streak_viewer["Id"] == message.author.id, "Streak"] += 1
            streak_viewer.loc[streak_viewer["Id"] == message.author.id, "Derniere Date de Connexion"] = date_stream
            val_exacte,proch_streak,proch_recompense = prochaine_recompense(message.author.id)
            if val_exacte != -1 and message.author.id not in self.liste_recompense:
                await message.channel.send(f"@{message.author.name}, Tu es a {streak_viewer.loc[streak_viewer['Viewer'] == message.author.name, 'Streak'].values[0]} visionnages consécutifs. Tu peux {recompense_streak.loc[recompense_streak['Streak'] == val_exacte, 'Récompense'].values[0]}.")
                self.liste_recompense.add(message.author.id)
        
        elif streak_viewer.loc[streak_viewer["Id"] == message.author.id, "Derniere Date de Connexion"].values[0] != date_stream  :
            streak_viewer.loc[streak_viewer["Id"] == message.author.id, "Streak"] = 1
            streak_viewer.loc[streak_viewer["Id"] == message.author.id, "Derniere Date de Connexion"] = date_stream
        new_announce = {
                "Viewer": message.author.name,
                "Streak": streak_viewer.loc[streak_viewer["Viewer"] == message.author.name, "Streak"].values[0]
            }
        annonce_streak = pd.concat([annonce_streak, pd.DataFrame([new_announce])], ignore_index=True)
        streak_viewer.to_csv("../data/streak viewer.txt", index=False, sep=";")
        await self.handle_commands(message)

        
  
bot = MyBot()
bot.run()       