'''
combat pokemon
on met des types, le joueur à des capacités
eau efficace contre feu, feu contre le vent, le ventre contre la terre, et la terre contre le vent
si efficace: x1.5 dégats, si pas efficace: x0.5 dégat
armure = reduction de dégats
sorts de base: 10 de dégats
'''
import discord
import sqlite3
import asyncio
from random import randint
from discord.ext import commands


class Foret(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.personne_en_combat = []
        self.attack_zombie = ['Charge', 'Clef de bras']
        self.PV_des_monstres = []
        self.nouveau_PV_monstres = []


    @commands.command(aliases=['ATTACK', 'attaque', 'ATTAQUE', 'attaquer', 'ATTAQUER'])
    async def attack(self, ctx):
        self.tag = str(ctx.author)[-5:]
        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        self.infos_joueurs = curseur.execute('SELECT * FROM joueurs').fetchall()
        connexion.close()

        for personnes in self.infos_joueurs:
            if personnes[0] == self.tag:
                if personnes[4] <= 10:
                    await ctx.send(f"{ctx.author.name}, nous savons tous que vous voulez impressionez votre mère avec vos talents d'escrimes, mais aller se battre contre des monstres avec si peu de vie est du suicide...")
                    return 0
                #combat debut
                '''
                règles des combats:
                chaque tour ne durera pas plus de 45 secondes, sinon tu perds
                si un des deux dueliste meurt, l'autre gagne
                la fuite est une option mais est déconseillée --> malédictions
                la mort = perte d'argent et la victoire = gain d'argent
                on a des attaques, si attaque inconnue --> supprime le message en 5 secondes
                élement avantageux sur d'autres
                '''
                if self.tag in self.personne_en_combat:
                    await ctx.send('Vous êtes déjà en combat...')
                    return 0

                self.personne_en_combat.append(self.tag)

                self.PV_NOUVEAU_MONSTRE = randint(40, 60)
                self.PV_des_monstres.append([self.tag, self.PV_NOUVEAU_MONSTRE, personnes[4], 0]) #on met toutes les infos dedans

                self.embed_zombie = discord.Embed(title=f':crossed_swords:__COMBAT ENTRE {ctx.author.name.upper()} ET UN ZOMBIE SAUVAGE__:crossed_swords:',
                                                  colour=discord.Color.orange())

                self.embed_zombie.add_field(name=f'__APYRE__    PV = {personnes[4]}', value=f"**__Compétences__**:\n{personnes[6].split(',')[0].split(':')[0]}, __Dégats__: {personnes[6].split(',')[0].split(':')[1]}\n{personnes[6].split(',')[1].split(':')[0]}, __Dégats__: {personnes[6].split(',')[1].split(':')[1]}", inline=True)
                self.embed_zombie.add_field(name=f"__ZOMBIE__    PV = {self.PV_NOUVEAU_MONSTRE}", value=f"**__Compétences__**:\n{self.attack_zombie[0]}, __Dégats__: 10\n{self.attack_zombie[1]}, __Dégats__: 10", inline=True)

                await ctx.send(embed=self.embed_zombie)
                await ctx.send(f"*{ctx.author}, un zombie arrive et vous parle dans une langue incompréhensible*")
                await ctx.send(
                    f"**C'est à vous d'attaquer en premier,\nvos attaques sont __{personnes[6].split(',')[0]}, {personnes[6].split(',')[1]}__**")
                            #CHANGEMENTS DES ATTAQUES 14/12 SI CA BUG VERIFIER ICI


                def check(m):
                    return (m.content.lower() == "lame d'air" and m.channel == channel and m.author == ctx.author) or (m.content.lower() == "voltige" and m.channel == channel and m.author == ctx.author) or \
                           (m.content.lower() == "bombe aquatique" and m.channel == channel and m.author == ctx.author) or (m.content.lower() == "typhon" and m.channel == channel and m.author == ctx.author) or \
                           (m.content.lower() == "brasier" and m.channel == channel and m.author == ctx.author) or (m.content.lower() == "déflagration" and m.channel == channel and m.author == ctx.author)

                    '''#les attaques 12 dégats:
                    if (m.content == "Lame d'air" and m.channel == channel and m.author == ctx.author) or (m.content == "Bombre aquatique" and m.channel == channel and m.author == ctx.author) or (m.content == "Déflagration" and m.channel == channel and m.author == ctx.author):
                        self.degats = 12
                        return True
                    elif (m.content == "Voltige" and m.channel == channel and m.author == ctx.author) or (m.content == "Brasier" and m.channel == channel and m.author == ctx.author):
                        self.degats = 10
                        return True
                    elif (m.content == "Typhon" and m.channel == channel and m.author == ctx.author):
                        self.degats = 11
                        return True
                    else:
                        return False'''


                while self.tag in self.personne_en_combat:
                    channel = ctx.channel

                    try:
                        msg = await self.client.wait_for('message', check=check, timeout=10.0)
                        #await channel.send(f"Vous venez d'attaquer **ZOMBIE** avec {msg.content} et lui infligez 10 points de dégats")

                        self.nouveau_PV_monstres = []
                        for combattants in self.PV_des_monstres:

                            if self.tag == combattants[0]:

                                if randint(0, 100) <= 10: #coup critique 10% de chance
                                    combattants[1] -= 10 #a changer quand on fera des dégats pour chaquue attaque
                                    await channel.send(f"{combattants[0]} MAGNIFIQUE COUP CRITIQUE AVEC VOTRE ATTAQUE {msg.content}, Vous lui infligez alors 20 points de dégats !")

                                else: #pas coup critique
                                    combattants[1] -= 10
                                    await channel.send(
                                        f"Vous venez d'attaquer **ZOMBIE** avec {msg.content} et lui infligez 10 points de dégats")

                                if combattants[1] > 0:
                                    self.degats = randint(3, 8)

                                    combattants[2] -= self.degats
                                    await channel.send(f"{ctx.author.name}, le zombie vous attaque également et vous inflige {self.degats} points de dégats\nIl vous reste {combattants[2]} PV")
                                    self.nouveau_PV_monstres.append(combattants)
                                if combattants[1] <= 0:
                                    self.nouveau_PV_monstres.append(combattants)


                        self.PV_des_monstres = self.nouveau_PV_monstres

                    except asyncio.TimeoutError: #perd a cause du temps #FONCTIONNE
                        await channel.send(f'{ctx.author.name}, votre temps est écoulé pour ce tour, vous fuyez vers le village et faites tomber une partie de votre argent sur le chemin')
                        self.joueur_a_supprimer = self.personne_en_combat[0]
                        self.parti_a_supprimer = self.PV_des_monstres[0]
                        self.personne_en_combat.remove(self.joueur_a_supprimer)
                        self.PV_des_monstres.remove(self.parti_a_supprimer)

                        for personne in self.infos_joueurs:
                            if personne[0] == self.joueur_a_supprimer:
                                self.argent = personne[2]

                        connexion = sqlite3.connect('base_donnes_bot_discord.db')
                        curseur = connexion.cursor()
                        curseur.execute('UPDATE joueurs SET PV = ? WHERE pseudo = ?', (self.parti_a_supprimer[2], self.joueur_a_supprimer))
                        curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (round(self.argent * 70 / 100), self.joueur_a_supprimer)) #le jour perd environ 30% de son argent
                        curseur.execute('UPDATE joueurs SET emplacement = ? WHERE pseudo = ?', ('village', self.joueur_a_supprimer))

                        connexion.commit()
                        connexion.close()

                    for combattants in self.PV_des_monstres: #un monstre arrive à 0

                        if combattants[1] <= 0: #si un mob est mort
                            self.pv = combattants[2]
                            self.PV_des_monstres.remove(combattants)
                            self.personne_en_combat.remove(combattants[0])

                            for personne in self.infos_joueurs:
                                if personne[0] == combattants[0]:
                                    self.argent = personne[2]
                            self.argent_plus = randint(25, 75)
                            await channel.send(f"Bravo {ctx.author.name}, vous avez tuer le zombie et remportez {self.argent_plus} yenis, vous avez encore {self.pv} PV ")
                            connexion = sqlite3.connect('base_donnes_bot_discord.db')
                            curseur = connexion.cursor()
                            curseur.execute('UPDATE joueurs SET pv = ? WHERE pseudo = ?', (self.pv, combattants[0]))
                            curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (self.argent + self.argent_plus, combattants[0]))

                            connexion.commit()
                            connexion.close()


                        if combattants[2] <= 0: #Si un joueur meurt, FONCTIONNE

                            self.PV_des_monstres.remove(combattants)
                            self.personne_en_combat.remove(combattants[0])

                            for personne in self.infos_joueurs:
                                if personne[0] == combattants[0]:
                                    self.argent = personne[2]

                            await channel.send(f"{ctx.author.name}, vous venez de mourir, et le monstre vous à complètement privés de vos biens, vous perdez une partie de votre argent et une unité compétente vous ramène chez vous")
                            connexion = sqlite3.connect('base_donnes_bot_discord.db')
                            curseur = connexion.cursor()
                            curseur.execute('UPDATE joueurs SET pv = ? WHERE pseudo = ?', (0, combattants[0]))
                            curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (round(self.argent * 95 / 100), combattants[0]))
                            curseur.execute('UPDATE joueurs SET emplacement = ? WHERE pseudo = ?', ('base', combattants[0]))
                            connexion.commit()
                            connexion.close()

def setup(client):
    client.add_cog(Foret(client))
#pour l'instant, rien