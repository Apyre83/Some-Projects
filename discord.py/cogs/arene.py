import sqlite3
import discord
import asyncio
from random import randint
from discord.ext import commands

class Arene(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.joueurs_attributs = [[], []]
        self.parties_en_cours = []
        self.capacites_joueurs = []

    @commands.command(aliases=['DUEL', 'Duel'])
    async def duel(self, ctx, bet):

        try:
            bet = int(bet)
            if int(bet) < 50:
                await ctx.send(f"{ctx.author.name}, tu dois parier au moins 50 yenis")
                return 0
        except ValueError:
            await ctx.send(f"{ctx.author.name}, je suis désolé de mon manque de culture, je ne parle pas l'héxadécimal, veuillez saisir votre mise avec un entier supérieur ou égal à 50")
            return 0

        self.personne = str(ctx.author)[-5:]
        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete1 = curseur.execute('SELECT * FROM joueurs')

        requete = requete1.fetchall()
        connexion.close()


        self.joueurs_attributs = [[], []]
        for personne in requete:
            if personne[0] == self.personne:
                for element in personne:
                    self.joueurs_attributs[0].append(element)
                self.joueurs_attributs[0].append(ctx.author.name)

                for parties_en_cours in self.parties_en_cours:
                    for joueur in parties_en_cours:
                        if self.personne == joueur[0]:

                            await ctx.send(f"__ERREUR__: Vous êtes déjà dans une partie !")
                            return 0

                if personne[2] < 50:
                    await ctx.send(f"{ctx.author.name}, Tu n'as pas parié assez d'__Argent__, il faut au moins 50 yenis pour un duel")
                    return 0
                if personne[2] < bet:
                    await ctx.send(f"{ctx.author.name}, Tu as parié beaucoup trop ! Tu ne possèdes pas autant d'argent !")
                    return 0

        await ctx.send(f"Le joueur {ctx.author} cherche un dueliste à sa hauteur !\nRejoins-le en tapant << rejoindre le combat >>")

        def check(m):
            if m.author != ctx.author and m.channel == ctx.channel and m.content.lower() == 'rejoindre le combat':
                for personne in requete:

                    if personne[0] == str(m.author)[-5:]:

                        if personne[2] < bet:
                            return False
                        else:
                            return True
        condition = False
        while condition == False:

            try: #obtenir le 2eme joueur
                self.reponse = await self.client.wait_for('message', check=check, timeout=60.0)
                condition = True
                self.joueurs_attributs[1] = []
                for parties_en_cours in self.parties_en_cours:
                    for joueur in parties_en_cours:
                        if joueur[0] == str(self.reponse.author)[-5:]:
                            condition = False
                            await ctx.send(f"{self.reponse.author}, __ERREUR__: Vous êtes déjà dans une partie !")

                for personne in requete:
                    if str(personne[0]) == str(self.reponse.author)[-5:]:

                        for element in personne:
                            self.joueurs_attributs[1].append(element)
                        self.joueurs_attributs[1].append(self.reponse.author.name)

            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.name}, personne n'a rejoint votre duel, quel dommage !")
                return 0

        self.partie = [self.joueurs_attributs[0], self.joueurs_attributs[1]]
        self.parties_en_cours.append(self.partie)


        #           CREATION DU EMBED POUR PRESENTER LE COMBAT
        self.embed_presentation = discord.Embed(title=f":crossed_swords:__DUEL ENTRE 2 CHEVALIERS QUELCONQUES__:crossed_swords:",
                                                description=f":money_with_wings:ARGENT EN JEU: {bet * 2} $:money_with_wings:",
                                                color=discord.Color.orange())
        self.embed_presentation.add_field(
            name=f'__{self.parties_en_cours[len(self.parties_en_cours) - 1][0][7]}__    PV = {self.parties_en_cours[len(self.parties_en_cours) - 1][0][4]}\nELEMENT: __{self.parties_en_cours[len(self.parties_en_cours) - 1][0][5].upper()}__',
            value=f"**__Compétences__**:\n\n**{self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[0][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[0][1:].lower()}**, __Dégats__: {self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[1][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[1][1:].lower()},\nType **__{self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[2].upper()}__**\n**{self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[0][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[0][1:].lower()}**, __Dégats__: {self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[1][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[1][1:].lower()},\nType **__{self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[2].upper()}__**",
            inline=True)

        self.embed_presentation.add_field(
            name=f'__{self.parties_en_cours[len(self.parties_en_cours) - 1][1][7]}__    PV = {self.parties_en_cours[len(self.parties_en_cours) - 1][1][4]}\nELEMENT: __{self.parties_en_cours[len(self.parties_en_cours) - 1][1][5].upper()}__',
            value=f"**__Compétences__**:\n\n**{self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[0][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[0][1:].lower()}**, __Dégats__: {self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[1][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[1][1:].lower()},\nType **__{self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[2].upper()}__**\n**{self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[0][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[0][1:].lower()}**, __Dégats__: {self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[1][0].upper() + self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[1][1:].lower()},\nType **__{self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[2].upper()}__**",
            inline=True)

        self.embed_presentation.set_footer(text=f"La fuite est une option mais apporte de nombreux handicaps")
        await ctx.send(embed=self.embed_presentation)

        #           EMBED A MODIFIER POUR CHAQUE ACTIONS DANS LE COMBAT
        self.embed_partie = discord.Embed(title = f"__LE DUEL__:",
                                          color=discord.Color.orange())

        self.embed_partie.add_field(name=f'__{self.parties_en_cours[len(self.parties_en_cours) - 1][0][7]}__    PV = {self.parties_en_cours[len(self.parties_en_cours) - 1][0][4]}\nELEMENT: __{self.parties_en_cours[len(self.parties_en_cours) - 1][0][5].upper()}__', value=':crossed_swords:DEBUT DU COMBAT:crossed_swords:', inline=True)
        self.embed_partie.add_field(name=f"__{self.parties_en_cours[len(self.parties_en_cours) - 1][1][7]}__    PV = {self.parties_en_cours[len(self.parties_en_cours) - 1][1][4]}\nELEMENT: __{self.parties_en_cours[len(self.parties_en_cours) - 1][1][5].upper()}__", value=':crossed_swords:DEBUT DU COMBAT:crossed_swords:', inline=True)

        self.embed_partie.set_footer(text=f"TOUR 1:\nC'est à {self.parties_en_cours[len(self.parties_en_cours) - 1][0][7]} de jouer !")
        self.embed_message_debut = await ctx.send(embed=self.embed_partie)

        self.capacites_joueurs.append([[[self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[0],
                                    int(self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[1][:-7]),
                                         self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[0].split(':')[2]],
                                   [self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[0],
                                    int(self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[1][:-7]),
                                    self.parties_en_cours[len(self.parties_en_cours) - 1][0][6].split(',')[1].split(':')[2]]],
                                  [[self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[0],
                                    int(self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[1][:-7]),
                                    self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[0].split(':')[2]],
                                   [self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[0],
                                    int(self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[1][:-7]),
                                    self.parties_en_cours[len(self.parties_en_cours) - 1][1][6].split(',')[1].split(':')[2]]]])


        #Le duel commence ici
        #ELEMENTS: FEU --> AIR; AIR --> TERRE; TERRE --> EAU; EAU --> FEU
        #Efficacités = 1.5x dégats; Résistances = 0.5 dégats;
        #Coups critiques: 10% de chance de critique --> X2 dégats
        #Joueur 1: attaque en premier
        #Un joueur meurt: le gagnant, récupère la mise (le bet); Le joueur mort: retourne a 50% de ses hp et le gagnant retourne à 75% de ses hp max
        #Si un joueur fuit, il doit payer 10% de sa mise au gagnant, il peut devenir endêtté
        combat = True
        self.tour = 1
        #                                    0       1       2         3        4      5         6        7
        while combat: #attributs_joueurs: [pseudo, niveau, argent, emplacement, pv, element, capacites, pseudo]

            def check_joueur1(m):
                indice = 0
                for parties_en_cours in self.parties_en_cours:
                    if parties_en_cours[0][0] == str(m.author)[-5:]:

                        for i in range(2):
                            if m.content.lower() == self.capacites_joueurs[indice][0][i][0] or m.content.lower() == 'fuite':
                                return True
                    indice += 1
                return False

            def check_joueur2(m):
                indice = 0
                for parties_en_cours in self.parties_en_cours:
                    if parties_en_cours[1][0] == str(m.author)[-5:]:
                        for i in range(2):
                            if m.content.lower() == self.capacites_joueurs[indice][1][i][0] or m.content.lower() == 'fuite':
                                return True

                    indice += 1
                return False

            '''<-----------------------------------------------------------------TOUR DU JOUEUR 1------------------------------------------------------------------------------------->'''

            try: #Tour du joueur 1  //   Pour récuperer l'attaque du joueur 1

                msg = await self.client.wait_for('message', check=check_joueur1, timeout=60.0)

            except asyncio.TimeoutError:#perdre à cause du temps
                for parties_en_cours in self.parties_en_cours:
                    if parties_en_cours[0][0] == str(ctx.author)[-5:]:
                        await ctx.send(f"{parties_en_cours[1][7]} a gagné la partie car {parties_en_cours[0][7]} a épuisé tout son temps !")
                        self.effectuer_argent(parties_en_cours[1][0], parties_en_cours[0][0], parties_en_cours[1][2], parties_en_cours[0][2], bet)
                        self.parties_en_cours.remove(parties_en_cours)
                        return 0

            #l'attaque se lance
            indice = 0
            for parties_en_cours in self.parties_en_cours:
                if parties_en_cours[0][0] == str(msg.author)[-5:]:
                    if msg.content.lower() == 'fuite':
                        self.indice = indice
                        await ctx.send(
                            f"{self.parties_en_cours[self.indice][0][7]} prend la fuite, le gagnant est donc {self.parties_en_cours[self.indice][1][7]}")
                        self.effectuer_argent(self.parties_en_cours[self.indice][1][0],
                                              self.parties_en_cours[self.indice][0][0],
                                              self.parties_en_cours[self.indice][1][2],
                                              self.parties_en_cours[self.indice][0][2], bet)
                        self.parties_en_cours.remove(self.parties_en_cours[self.indice])
                        print("fuite+")
                        return 0


                    for i in range(2):
                        if msg.content.lower() == self.capacites_joueurs[indice][0][i][0]:
                            self.indice = indice
                            self.degats = self.capacites_joueurs[indice][0][i][1]
                            self.attribut_attaque = self.capacites_joueurs[indice][0][i][2]
                            self.attribut_defenseur = self.parties_en_cours[indice][1][5]

                indice += 1

            self.message_ligne1 = f"{self.parties_en_cours[self.indice][0][7]} utilise {msg.content.upper()[0] + msg.content.lower()[1:]}"
            self.message_ligne2 = f"{self.parties_en_cours[self.indice][1][7]} perd alors {self.degats} PV"

            if randint(1, 100) <= 10: #coup critique
                self.degats *= 1.5
                self.message = "**COUP CRITIQUE** !\n" + self.message_ligne1


            if self.est_efficace(self.attribut_attaque, self.attribut_defenseur) == True:
                self.degats *= 2
                self.message_ligne1 = (self.message_ligne1 + " et c'est super efficace !").upper()

            elif self.est_efficace(self.attribut_attaque, self.attribut_defenseur) != 0:
                print('a')
                self.degats = round(self.degats / 2)
                self.message_ligne1 = self.message_ligne1 + " mais ce n'est pas très efficace..."

            self.message = f"{self.message_ligne1}\n{self.message_ligne2}"
            self.message = self.message[:-5] + f"{self.degats} PV"


            if randint(1, 100) <= 7: #esquive
                self.message = f"Incroyable,\n{self.parties_en_cours[self.indice][1][7]} fait preuve d'agiliter et esquive l'attaque !"
                self.degats = 0

            #   ON EFFECTUE LES CHANGEMENTS:

            self.parties_en_cours[self.indice][1][4] -= self.degats
            if self.parties_en_cours[self.indice][1][4] <= 0:
                self.effectuer_argent(self.parties_en_cours[self.indice][0][0], self.parties_en_cours[self.indice][1][0],
                                      self.parties_en_cours[self.indice][0][2], self.parties_en_cours[self.indice][1][2], bet)
                self.message = f"{self.message_ligne1}\n{self.message_ligne2} ET MEURT SUR LE COUP !!\nVICTOIRE DE {self.parties_en_cours[self.indice][0][7]}"


            # NOUVEAU MESSAGE MISE EN FORME
            self.embed_message_modifie = discord.Embed(title=f"__LE DUEL__:",
                                              color=discord.Color.orange())

            self.embed_message_modifie.add_field(
                name=f'__{self.parties_en_cours[self.indice][0][7]}__    PV = {self.parties_en_cours[self.indice][0][4]}\nELEMENT: __{self.parties_en_cours[self.indice][0][5].upper()}__',
                value=self.message, inline=True)
            self.embed_message_modifie.add_field(
                name=f"__{self.parties_en_cours[self.indice][1][7]}__    PV = {self.parties_en_cours[self.indice][1][4]}\nELEMENT: __{self.parties_en_cours[self.indice][1][5].upper()}__",
                value='EN TRAIN DE CHOISIR SON ATTAQUE...', inline=True)

            self.embed_message_modifie.set_footer(
                text=f"TOUR {self.tour}:\nC'est à {self.parties_en_cours[self.indice][1][7]} de jouer !")

            await ctx.channel.purge(limit=1)#on clear le message envoyé pour connaitre l'attaque
            await self.embed_message_debut.edit(embed=self.embed_message_modifie)#on modifie le embed de la partie

            self.tour += 1
            if self.parties_en_cours[self.indice][1][4] <= 0: #on quitte si mort
                self.parties_en_cours.remove(self.parties_en_cours[self.indice])
                return 0

            '''-----------------------------------------------------JOUEUR 2 DOIT JOUER--------------------------------------------------------------------------------------------'''

            try: #Tour joueur 2   //    Pour récuperer l'attaque du joueur 2
                msg = await self.client.wait_for('message', check=check_joueur2, timeout=60.0)

            except asyncio.TimeoutError:#perdre à cause du temps
                for parties_en_cours in self.parties_en_cours:
                    if parties_en_cours[0][0] == str(ctx.author)[-5:]:
                        await ctx.send(
                            f"{parties_en_cours[0][7]} a gagné la partie car {parties_en_cours[1][7]} a épuisé tout son temps !")
                        self.effectuer_argent(parties_en_cours[1][0], parties_en_cours[0][0], parties_en_cours[1][2],
                                              parties_en_cours[0][2], bet)
                        self.parties_en_cours.remove(parties_en_cours)
                        return 0

            indice = 0
            for parties_en_cours in self.parties_en_cours:
                if parties_en_cours[1][0] == str(msg.author)[-5:]: #probleme ici, on ne detecte pas le joueur qui joue
                    if msg.content.lower() == 'fuite':
                        self.indice = indice
                        await ctx.send(
                            f"{self.parties_en_cours[self.indice][1][7]} prend la fuite, le gagnant est donc {self.parties_en_cours[self.indice][0][7]}")
                        self.effectuer_argent(self.parties_en_cours[self.indice][0][0],
                                              self.parties_en_cours[self.indice][1][0],
                                              self.parties_en_cours[self.indice][0][2],
                                              self.parties_en_cours[self.indice][1][2], bet)
                        self.parties_en_cours.remove(self.parties_en_cours[self.indice])
                        return 0

                    for i in range(2):
                        if msg.content.lower() == self.capacites_joueurs[indice][1][i][0]:

                            self.indice = indice
                            self.degats = self.capacites_joueurs[indice][1][i][1]
                            self.attribut_attaque = self.capacites_joueurs[indice][1][i][2]
                            self.attribut_defenseur = self.parties_en_cours[indice][0][5]

                indice += 1

            self.message_ligne1 = f"{self.parties_en_cours[self.indice][1][7]} utilise {msg.content.upper()[0] + msg.content.lower()[1:]}"
            self.message_ligne2 = f"{self.parties_en_cours[self.indice][0][7]} perd alors {self.degats} PV"

            if randint(1, 100) <= 10:  # coup critique
                self.degats *= 1.5
                self.message = "**COUP CRITIQUE** !\n" + self.message_ligne1

            if self.est_efficace(self.attribut_attaque, self.attribut_defenseur) == True:
                self.degats *= 2
                self.message_ligne1 = (self.message_ligne1 + " et c'est super efficace !").upper()

            elif self.est_efficace(self.attribut_attaque, self.attribut_defenseur) != 0:
                self.degats = round(self.degats / 2)
                self.message_ligne1 = self.message_ligne1 + " mais ce n'est pas très efficace..."

            self.message = f"{self.message_ligne1}\n{self.message_ligne2}"
            self.message = self.message[:-5] + f"{self.degats} PV"

            if randint(1, 100) <= 7:  # esquive
                self.message = f"Incroyable,\n{self.parties_en_cours[self.indice][0][7]} fait preuve d'agiliter et esquive l'attaque !"
                self.degats = 0

            #   ON EFFECTUE LES CHANGEMENTS:

            self.parties_en_cours[self.indice][0][4] -= self.degats
            if self.parties_en_cours[self.indice][0][4] <= 0:
                self.effectuer_argent(self.parties_en_cours[self.indice][1][0],
                                      self.parties_en_cours[self.indice][0][0],
                                      self.parties_en_cours[self.indice][1][2],
                                      self.parties_en_cours[self.indice][0][2], bet)
                self.parties_en_cours.remove(self.parties_en_cours[self.indice])
                self.message = f"{self.message_ligne1}\n{self.message_ligne2} ET MEURT SUR LE COUP !!\nVICTOIRE DE {self.parties_en_cours[self.indice][1][7]}"

            # NOUVEAU MESSAGE MISE EN FORME
            self.embed_message_modifie = discord.Embed(title=f"__LE DUEL__:",
                                                       color=discord.Color.orange())

            self.embed_message_modifie.add_field(
                name=f'__{self.parties_en_cours[self.indice][0][7]}__    PV = {self.parties_en_cours[self.indice][0][4]}\nELEMENT: __{self.parties_en_cours[self.indice][0][5].upper()}__',
                value="EN TRAIN DE CHOISIR SON ATTAQUE...", inline=True)
            self.embed_message_modifie.add_field(
                name=f"__{self.parties_en_cours[self.indice][1][7]}__    PV = {self.parties_en_cours[self.indice][1][4]}\nELEMENT: __{self.parties_en_cours[self.indice][1][5].upper()}__",
                value=self.message, inline=True)

            self.embed_message_modifie.set_footer(
                text=f"TOUR {self.tour}:\nC'est à {self.parties_en_cours[self.indice][0][7]} de jouer !")

            await ctx.channel.purge(limit=1)  # on clear le message envoyé pour connaitre l'attaque
            await self.embed_message_debut.edit(embed=self.embed_message_modifie)  # on modifie le embed de la partie

            self.tour += 1
            if self.parties_en_cours[self.indice][0][4] <= 0:  # on quitte si mort
                self.parties_en_cours.remove(self.parties_en_cours[self.indice])
                return 0


    def est_efficace(self, elementAttaquant, elementDefenseur):

        if elementAttaquant == 'eau':
            if elementDefenseur == 'feu':
                return True
            elif elementDefenseur == 'terre':
                return False
            else:
                return 0

        elif elementAttaquant == 'feu':
            if elementDefenseur == 'air':
                return True
            elif elementDefenseur == 'eau':
                return False
            else:
                return 0

        elif elementAttaquant == 'air':
            if elementDefenseur == 'terre':
                return True
            elif elementDefenseur == 'feu':
                return False
            else:
                return 0

        elif elementAttaquant == 'terre':
            if elementDefenseur == 'eau':
                return True
            elif elementDefenseur == 'air':
                return False
            else:
                return 0

    def effectuer_argent(self, gagnant, perdant, argent_gagnant, argent_perdant, mise):
        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        print(gagnant, perdant)
        curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (argent_gagnant + mise, gagnant))
        curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (argent_perdant - mise, perdant))
        curseur.execute('UPDATE joueurs SET pv = ? WHERE pseudo = ?', (50, perdant))
        curseur.execute('UPDATE joueurs SET pv = ? WHERE pseudo = ?', (75, gagnant))
        connexion.commit()
        connexion.close()

def setup(client):
    client.add_cog(Arene(client))