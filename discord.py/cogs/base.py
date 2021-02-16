import discord
import sqlite3
from discord.ext import commands

class base(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['RECRUTER', 'former', 'FORMER', 'recruit', 'RECRUIT'])
    async def recruter(self, ctx, genre, nombre): #chevaliers = 10 euros, geants = 15, mages = 20
        self.personne = str(ctx.author)[-5:]
        try:
            self.nombre = int(nombre)
        except Exception:
            await ctx.send("Afin d'éviter de créer des troupes avec 1 bras ou autre, tu dois indiquer le nombre de troupe à former en CHIFFRE\nLa commande est: '!recruter <type_de_troupe> <nombre>' !")
            return 0

        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT pseudo, argent, emplacement FROM joueurs')

        for personnes in requete.fetchall():
            if self.personne == personnes[0]:
                if personnes[2].lower() == 'base':

                    if genre.lower() == 'chevaliers': #si chevalier:

                        if self.nombre * 10 > personnes[1]: #si pas assez d'argent:
                            await ctx.send("Erreur lors de la création de troupes, Raison :\n--> Vous n'avez pas assez d'argent !")

                        else:
                            self.new_argent = personnes[1] - self.nombre * 10

                            curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (self.new_argent, self.personne))

                            self.nb_chevaliers = curseur.execute('SELECT pseudos, chevaliers FROM troupes')
                            for personne in self.nb_chevaliers.fetchall():
                                if personne[0] == self.personne:
                                    self.nouvelle_troupe = personne[1] + self.nombre
                                    curseur.execute('UPDATE troupes SET chevaliers = ? WHERE pseudos = ?', (self.nouvelle_troupe, self.personne))
                                    connexion.commit()

                            await ctx.send(f"{self.personne}, tu viens de former {self.nombre} chevaliers pour {self.nombre * 10} yenis.")

                    elif genre.lower() == 'geants':
                        if self.nombre * 15 > personnes[1]: #si pas assez d'argent:
                            await ctx.send("Erreur lors de la création de troupes, Raison :\n--> Vous n'avez pas assez d'argent !")

                        else:
                            self.new_argent = personnes[1] - self.nombre * 15

                            curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                            (self.new_argent, self.personne))

                            self.nb_geants = curseur.execute('SELECT pseudos, geants FROM troupes')

                            for personne in self.nb_geants.fetchall():
                                if personne[0] == self.personne:
                                    self.nouvelle_troupe = personne[1] + self.nombre
                                    curseur.execute('UPDATE troupes SET geants = ? WHERE pseudos = ?',
                                                    (self.nouvelle_troupe, self.personne))
                                    connexion.commit()
                            await ctx.send(f"{self.personne}, tu viens de former {self.nombre} géants pour {self.nombre * 15} yenis")

                    elif genre.lower() == 'mages':
                        if self.nombre * 20 > personnes[1]: #si pas assez d'argent:
                            await ctx.send("Erreur lors de la création de troupes, Raison :\n--> Vous n'avez pas assez d'argent !")

                        else:
                            self.new_argent = personnes[1] - self.nombre * 20

                            curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                            (self.new_argent, self.personne))

                            self.nb_mages = curseur.execute('SELECT pseudos, mages FROM troupes')

                            for personne in self.nb_mages.fetchall():
                                if personne[0] == self.personne:
                                    self.nouvelle_troupe = personne[1] + self.nombre
                                    curseur.execute('UPDATE troupes SET mages = ? WHERE pseudos = ?',
                                                    (self.nouvelle_troupe, self.personne))
                                    connexion.commit()

                            await ctx.send(f"{self.personne}, tu viens de former {self.nombre} mages pour {self.nombre * 20} yenis")
                    else:
                        await ctx.send("La troupe que tu as marqué n'existe pas, tu dois choisir entre 'Chevaliers', 'Geants' ou 'Mages'.")

                else:
                    await ctx.send('Erreur lors de la création de troupes, Raison :\n--> Vous ne vous trouvez pas à votre base !')

        connexion.close()

    @commands.command(aliases=['CONSTRUIRE', 'build', 'BUILD', 'craft', 'CRAFT'])
    async def construire(self, ctx, objet):
        self.personne = str(ctx.author)[-5:]
        self.objet = str(objet)

        connexion = sqlite3.connect('base_donnes_bot_discord.db')
        curseur = connexion.cursor()
        requete = curseur.execute('SELECT * FROM mines')
        for personnes in requete:
            if personnes[0] == self.personne:
                self.les_mines = personnes
        requete = curseur.execute('SELECT pseudo, argent, emplacement FROM joueurs')

        for element in requete.fetchall():
            if element[0] == self.personne:
                if element[2].lower() == 'base':
                    self.argent = element[1]

                    #Ici, le joueur veut construire. en partant de la premiere mine,
                    #qu'on en voit pas à -1, on regarde la prochaine. Les prix sont:
                    #[70, 1000, 145000, 4.6 millions, 1 milliard]



                    if self.objet.lower() == 'mineur': #si construction de mine
                        if self.les_mines[1] == -1: #1ere mine
                            if self.argent >= 70:
                                self.new_argent = self.argent - 70

                                curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?', (self.new_argent, self.personne))
                                connexion.commit()
                                curseur.execute('UPDATE mines SET mine1 = ? WHERE pseudo = ?', (0, self.personne))
                                connexion.commit()
                                connexion.close()
                                await ctx.send('Vous venez de construire votre premier mineur !')
                                return 0
                            else:
                                await ctx.send("Vous n'avez pas assez d'argent !")


                        elif self.les_mines[2] == -1:
                            if self.argent >= 1000:
                                self.new_argent = self.argent - 1000

                                curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                                (self.new_argent, self.personne))
                                connexion.commit()
                                curseur.execute('UPDATE mines SET mine2 = ? WHERE pseudo = ?', (0, self.personne))
                                connexion.commit()
                                connexion.close()
                                await ctx.send('Vous venez de construire votre deuxieme mineur !')
                                return 0

                            else:
                                await ctx.send("Vous n'avez pas assez d'argent !")

                        elif self.les_mines[3] == -1:
                            if self.argent >= 145000:
                                self.new_argent = self.argent - 145000

                                curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                                (self.new_argent, self.personne))
                                connexion.commit()
                                curseur.execute('UPDATE mines SET mine3 = ? WHERE pseudo = ?', (0, self.personne))
                                connexion.commit()
                                connexion.close()
                                await ctx.send('Vous venez de construire votre troisième mineur !')
                                return 0

                            else:
                                await ctx.send("Vous n'avez pas assez d'argent !")

                        elif self.les_mines[4] == -1:
                            if self.argent >= 4600000:
                                self.new_argent = self.argent - 4600000

                                curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                                (self.new_argent, self.personne))
                                connexion.commit()
                                curseur.execute('UPDATE mines SET mine4 = ? WHERE pseudo = ?', (0, self.personne))
                                connexion.commit()
                                connexion.close()
                                await ctx.send('Vous venez de construire votre quatrième mineur !')
                                return 0

                            else:
                                await ctx.send("Vous n'avez pas assez d'argent !")

                        elif self.les_mines[5] == -1:
                            if self.argent >= 1000000000:
                                self.new_argent = self.argent - 1000000000

                                curseur.execute('UPDATE joueurs SET argent = ? WHERE pseudo = ?',
                                                (self.new_argent, self.personne))
                                connexion.commit()
                                curseur.execute('UPDATE mines SET mine5 = ? WHERE pseudo = ?', (0, self.personne))
                                connexion.commit()
                                connexion.close()
                                await ctx.send('Vous venez de construire votre dernier mineur !')
                                return 0

                            else:
                                await ctx.send("Vous n'avez pas assez d'argent !")

                        else:
                            await ctx.send('Vous avez déjà construit tout vos mineurs !')
                            return 0

                    else:
                        await ctx.send("**__ERREUR__**: le bâtiment que vous voulez construire n'existe pas. Consulter __+help__ pour plus d'infos")
                else:
                    await ctx.send(f'Erreur lors de la construction, vous ne vous situez pas à votre base, {self.personne}')
        connexion.close()

def setup(client):
    client.add_cog(base(client))