import discord
import sqlite3
import asyncio
from discord.ext import commands


class Joueur(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.destinations = ['foret', 'base', 'village', 'arene']
        self.place = self.destinations[2]
        self.elements = ['feu', 'Feu', 'FEU', 'air', 'Air', 'AIR', 'eau', 'Eau', 'EAU', 'terre', 'Terre', 'TERRE']
        #stats:

    @commands.command(aliases=['jouer', 'debut', 'PLAY', 'JOUER', 'DEBUT'])
    async def play(self, ctx): #Fonction pour jouer la premiere fois // permet d'inscrire le joueur dans la base de données
        self.tag = str(ctx.author)[-5:]
        connexion = sqlite3.connect('base_donnes_bot_discord.db') #connexion base SQLITE
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT * FROM joueurs') #selectionner toute la table
        self.liste_pseudos = []


        for pseudos in requete.fetchall():
            self.liste_pseudos.append(pseudos[0])
        connexion.close()
        if self.tag in self.liste_pseudos:
            await ctx.send(f'Deja enregistré, {ctx.author}')

        else:
            await ctx.send(f"Alors comme ça tu décides de partir à l'aventure, {ctx.author}\nAvant de partir, sache que de nombreux sorciers abritent ce monde alors moi, pour éviter de te laisser mourir le premier jour, je vais t'attribuer un élément magique parmi:\n:fire:__LE FEU__:fire: - :cloud_tornado:__L'AIR__:cloud_tornado: - :earth_asia:__LA TERRE__:earth_asia: - :ocean:__L'EAU__:ocean:\nEvidemment, les éléments ont des spécificités et sont difficiles à maitriser alors, fais le bon choix !\n*Entrer le nom d'un élément en moins de 60 secondes:*")

            def check(m):#condition message utilisateur + element
                if m.content in self.elements:
                    if m.author == ctx.author:
                        return True

            try:
                msg = await self.client.wait_for('message', check=check, timeout=60.0) #si check = False: recommancer
                self.element = str(msg.content).lower()
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author}, TU N'AS PAS ENTRE LE NOM D'UN ELEMENT EN MOINS DE 60 SECONDES, RESSAYE")

            if self.element == 'feu':
                self.capacites = "déflagration:12 dégats:feu,brasier:10 dégats:feu"
            elif self.element == 'air':
                self.capacites = "lame d'air:12 dégats:air,voltige:10 dégats:air"
            elif self.element == 'eau':
                self.capacites = "bombe aquatique:12 dégats:eau,typhon:11 dégats:eau"
            else:
                self.capacites = "fracture tectonique:13 dégats:terre,poing de granite:12 dégats:terre"

            connexion = sqlite3.connect("base_donnes_bot_discord.db")
            curseur = connexion.cursor()

            curseur.execute('INSERT INTO joueurs (pseudo, niveau, argent, emplacement, PV, element, capacites) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (self.tag, 1, 100, 'village', 100, self.element, self.capacites))
            curseur.execute('INSERT INTO troupes (pseudos, chevaliers, geants, mages) VALUES (?, ?, ?, ?)',
                            (self.tag, 0, 0, 0))

            curseur.execute('INSERT INTO mines (pseudo, mine1, mine2, mine3, mine4, mine5) VALUES (?, ?, ?, ?, ?, ?)',
                            (self.tag, -1, -1, -1, -1, -1))
            connexion.commit()

            connexion.close()
            await ctx.send(f"Bienvenue dans l'aventure, **{ctx.author.name}** !\nJe te conseille d'abord d'aller faire un tour à ta base et d'y construire ton premier mineur !")

    @commands.command(aliases=['stat', 'STATS', 'STAT', 'statistiques', 'STATISTIQUES', 'statistique', 'STATISTIQUE'])
    async def stats(self, ctx):
        self.personne = str(ctx.author)[-5:]
        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT * FROM joueurs')

        for personnes in requete.fetchall():
            if self.personne == personnes[0]:
                self.embed = discord.Embed(
                    title = f'__{ctx.author} stats__:',
                    color = discord.Color.orange()
                )

                self.embed.set_thumbnail(url=ctx.author.avatar_url)

                self.embed.add_field(name=f'__Niveau__:', value=f"Tu es niveau {personnes[1]}", inline=False)
                self.embed.add_field(name=f'__Argent__:', value=f"Tu possèdes {personnes[2]} yenis", inline=False)
                self.embed.add_field(name=f'__Location__:', value=f"Tu te trouves ici: {personnes[3].upper()}", inline=False)
                self.embed.add_field(name='__POINTS DE VIE__', value=f"Tes points de vie sont à {personnes[4]}", inline=False)
                await ctx.send(embed=self.embed)
        connexion.close()

    @commands.command(aliases=['ARMY', 'armé', 'ARMÉ', 'armée', 'ARMÉE', 'arme', 'ARME'])
    async def army(self, ctx):
        self.personne = str(ctx.author)[-5:]

        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT * FROM troupes')

        for personnes in requete.fetchall():
            if personnes[0] == self.personne:
                self.embed = discord.Embed(
                    title=f'__Armée de {ctx.author}__:',
                    color=discord.Color.orange()
                )

                self.embed.set_thumbnail(url=ctx.author.avatar_url)

                self.embed.add_field(name=f'__Chevaliers__:', value=f"Tu possèdes {personnes[1]} chevaliers", inline=False)
                self.embed.add_field(name=f'__Géants__:', value=f"Tu possèdes {personnes[2]} géants", inline=False)
                self.embed.add_field(name=f'__Mages__:', value=f"Tu possèdes {personnes[3]} mages", inline=False)
                await ctx.send(embed=self.embed)
        connexion.close()

    @commands.command(aliases=['MINEUR', 'mineurs', 'MINEURS', 'mine', 'MINE', 'mines', 'MINES'])
    async def mineur(self, ctx):
        self.personne = str(ctx.author)[-5:]

        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT * FROM mines')

        for personnes in requete.fetchall():
            if personnes[0] == self.personne:
                self.embed = discord.Embed(
                    title = f"__Mineurs de {ctx.author}__",
                    color = discord.Color.orange()
                )

                self.embed.set_thumbnail(url=ctx.author.avatar_url)
                for i in range(5):
                    if personnes[i + 1] == -1:
                        self.embed.add_field(name=f'__Mineur #{i + 1}__:', value='Pas encore construit', inline=False)
                    else:
                        self.embed.add_field(name=f'__Mineur #{i + 1}__:', value=f'Valeur marchande de {personnes[i + 1]} yenis', inline=False)
                await ctx.send(embed=self.embed)
        connexion.close()

    @commands.command(aliases=['GOTO', 'gt', 'GT', 'go', 'Go', 'GO'])
    async def goto(self, ctx, message):
        self.personne = str(ctx.author)[-5:]

        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT pseudo, emplacement FROM joueurs')

        for personnes in requete.fetchall():
            if self.personne == personnes[0]:

                if message.lower() in self.destinations:
                    if personnes[1] == message.lower():
                        await ctx.send('Vous vous situez déjà ici !')

                    else:
                        await ctx.send(f'*Le joueur {ctx.author} se déplace vers {message.upper()}*')
                        curseur.execute('Update joueurs set emplacement = ? where pseudo = ?', (message.lower(), self.personne))
                        connexion.commit()
                        if message.lower() == 'foret':
                            await ctx.send(f"*Faites attention, {self.personne}, de nombreux zombies grouillent là-bas...*")

                else:
                    await ctx.send(f"{ctx.author}, destination non connue, vérifiez l'orthographe à moins que vous vous soyez trompez d'endroit !")

        connexion.close()


def setup(client):
    client.add_cog(Joueur(client))