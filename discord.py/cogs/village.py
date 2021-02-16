import discord
import sqlite3
import asyncio
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.capacites = [["lame d'air,12 dégats,0", "voltige,10 dégats,0", "rush aerien,21 dégats,1000", "flash Dash,27 dégats,53 000"],
                          ["déflagration,12 dégats,0", "brasier,10 dégats,0", "eruption cutannée,22 dégats,1200", "explosion diabolique,43 dégats,150 000"],
                          ["bombe aquatique,12 dégats,0", "typhon,11 dégats,0", "aquajet,22 dégats,1200", "déchainement marin,32 dégats,70 000"],
                          ["fracture tectonique,13 dégats,0", "poing de granite,12 dégats,0", "eboulement d'acier,23 dégats,1450", "rafale tellurique,35 dégats,100 000"]]

        self.element = ['air', 'feu', 'eau', 'terre']


    @commands.command(aliases=['SELL', 'vendre', 'VENDRE'])
    async def sell(self, ctx, la_mine):
        self.personne = str(ctx.author)[-5:]

        if not(len(la_mine) == 3 or len(la_mine) == 4 or len(la_mine) == 5):
            await ctx.send(f"{ctx.author} ERREUR lors de la vente, veuillez consulter le __!HELP__ pour plus d'informations.")
            return 0

        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        table_mines = curseur.execute('SELECT * FROM mines').fetchall()
        table_argent = curseur.execute('SELECT pseudo, argent, emplacement FROM joueurs').fetchall()

        for items in table_argent:
            if items[0] == self.personne:
                self.place = items[2]

        if self.place.lower() == 'village':

            for items in table_argent:
                if items[0] == self.personne:
                    self.argent = items[1]
                    self.new_argent = 0

            if la_mine.lower() == 'all': #si on vend tout
                for personnes in table_mines:
                    if personnes[0] == self.personne:
                        for i in range(5):
                            if personnes[i+1] != -1:
                                self.new_argent += personnes[i+1]
                                curseur.execute(f'UPDATE mines SET mine{i+1} = ? WHERE pseudo = ?',
                                        (0, self.personne))
                                connexion.commit()

                        curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                        (self.argent + self.new_argent, self.personne))
                        connexion.commit()
                        await ctx.send(f"*{ctx.author}, vous venez de vendre toute votre marchandise pour {self.new_argent} yenis !*")

            elif la_mine.lower() == 'help':
                self.embed = discord.Embed(
                    title="__COMMENT FONCTIONNE LA VENTE__?",
                    color=discord.Color.orange()
                )

                self.embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                self.embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/784711456431276035/787334519018881095/image_argent.png')

                self.embed.add_field(name='__DANS LA MINE__:', value='Nos chers petits ouvriers, très pointilleux sur les horaires,\nramènent toutes les 30 secondes, des minerais différents\nen fonction de là où ils travaillent !', inline=False)
                self.embed.add_field(name='__MAIS QUELS SONT LES PRIX__?', value='__MINE 1__: 5 yenis / 30 secondes\n__MINE 2__: 240 yenis / 30 secondes\n__MINE 3__: 12 000 yenis / 30 secondes\n__MINE 4__: 150 000 yenis / 30 secondes\n__MINE 5__: 1 200 000 yenis / 30 secondes', inline=False)


                await ctx.send(embed=self.embed)

            elif la_mine[:4] == 'mine' and 1 <= int(la_mine[-1:]) <= 5:
                self.numero_mine = int(la_mine[-1:])
                for personnes in table_mines:
                    if personnes[0] == self.personne:
                        self.new_argent = personnes[self.numero_mine]
                        curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                        (self.new_argent + self.argent, self.personne))
                        curseur.execute(f'UPDATE mines SET mine{self.numero_mine} = ? WHERE pseudo = ?',
                                        (0, self.personne))

                        connexion.commit()
                        await ctx.send(f"*{ctx.author}, vous venez de vendre votre marchandise de mine{self.numero_mine} pour {self.new_argent} yenis !*")

            else:
                await ctx.send(f"{ctx.author} ERREUR lors de la vente, veuillez consulter le __!HELP__ pour plus d'informations.")

        else:
            await ctx.send(
                f"{ctx.author}, La vente en ligne n'existe pas dans notre petit village perdu, allez voir directement le commerçant __au village__ pour vendre votre marchandise !")

        connexion.close()


    #l'achat de capacitées
    @commands.command(aliases=['BUY', 'Buy', 'achat', 'ACHAT', 'Achat', 'acheter', 'Acheter', 'ACHETER'])
    async def buy(self, ctx, objet, *, message):
        self.personne = str(ctx.author)[-5:]

        def check(m):
            return (m.author == ctx.author and m.content == '1') or (m.author == ctx.author and m.content == '2')

        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT * FROM joueurs').fetchall()
        connexion.close()

        for personnes in requete:
            if personnes[0] == self.personne:
                self.table = personnes

        id_element = 0
        if objet.lower() == 'capacité' or objet.lower() == 'capacités' or objet.lower() == 'capacitées':
            for element in self.capacites:
                id_attaque = 0
                for attaque in element:

                    if attaque.split(",")[0] == message.lower():
                        if self.table[2] >= int(self.capacites[id_element][id_attaque].split(",")[2]):
                            await ctx.send(f"Choisissez la capacité que vous voulez remplacer:\nTapez '1' pour supprimer {self.table[6].split(',')[0].split(':')[0]}"
                                           f" ou '2' pour supprimer {self.table[6].split(',')[1].split(':')[0]}")
                            try:
                                message = await self.client.wait_for('message', check=check, timeout=60.0)
                            except asyncio.TimeoutError:
                                await ctx.send(f"ERREUR: Vous avez mit trop de temps pour choisir la capacité à remplacer, veuillez réiterer votre demande.")
                                return 0


                            if message.content == '1':
                                self.nouveau_capacite = f"{self.capacites[id_element][id_attaque].split(',')[0]}:{self.capacites[id_element][id_attaque].split(',')[1]}:{self.element[id_element]},{self.table[6].split(',')[1]}"
                            else:
                                self.nouveau_capacite = f"{self.capacites[id_element][id_attaque].split(',')[0]}:{self.capacites[id_element][id_attaque].split(',')[1]}:{self.element[id_element]},{self.table[6].split(',')[0]}"

                            connexion = sqlite3.connect('base_donnes_bot_discord.db')
                            curseur = connexion.cursor()
                            curseur.execute('UPDATE joueurs SET capacites = ? WHERE pseudo = ?', (self.nouveau_capacite, self.personne))
                            curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (self.table[2] - int(self.capacites[id_element][id_attaque].split(",")[2]), self.personne))
                            connexion.commit()
                            connexion.close()

                            await ctx.send(f"{ctx.author.name} vient d'apprendre la capacité {self.capacites[id_element][id_attaque].split(',')[0].upper()} pour seulement {int(self.capacites[id_element][id_attaque].split(',')[2])} yenis !")
                            return 0

                        else:
                            await ctx.send(f"ERREUR: Vous n'avez pas assez d'argent, {ctx.author.name}")
                            return 0


                    id_attaque += 1
                id_element += 1

            await ctx.send(f"ERREUR:La capacité que vous avez chosie n'existe pas !")


def setup(client):
    client.add_cog(Test(client))