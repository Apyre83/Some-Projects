'''Ici est le cerveau du programme:
On récolte les infos des autres programmes (Joueur...) qu'on envoie ici pour tout traiter'''
import discord
import os
import sqlite3
from random import randint
from discord.ext import commands
from discord.ext import tasks

client = commands.Bot(command_prefix='+', help_command=None)#cela permet de savoir comment parler au bot (préfixe "!")
@client.event
async def on_ready(): #Lorsqu'il démarre
    print('Bot is ready !')
    generer_monnaie.start()
    print("t")

@client.command()
async def test(ctx, test, *, arg):
    await ctx.send(arg)

@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Erreur lors de la commande, vous avez oubliez un paramètre, tapez '__+help__' pour plus d'infos , {ctx.author} !")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"**ERREUR**: commande inconnue, tapez __+help__ pour plus d'informations.")

@client.command(aliases=['HELP', 'INFO', 'info', 'INFOS', 'infos', 'aide', 'AIDE', 'help 1', 'HELP 1', 'INFO 1', 'info 1', 'INFOS 1', 'infos 1', 'aide 1', 'AIDE 1'])
async def help(ctx):

    embed = discord.Embed(
        title = '__MENU HELP__:',
        description='Si tu comprends toujours rien, mp moi, Apyre#6893',
        colour = discord.Color.orange()
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/784711456431276035/787017845313503232/image_help.png')
    embed.add_field(name='__PLAY__:', value="Permet au joueur de partir à l'aventure, sauf si il est déjà parti...", inline=False)
    embed.add_field(name='__GOTO__:', value="-> goto <destination>\nPermet au joueur d'aller où il désire parmi:\nVillage, Base, Foret, Arene.", inline=False)
    embed.add_field(name='__STATS__:', value='Renvoie les statistiques du joueur', inline=False)
    embed.add_field(name='__ARMY__:', value="Renvoie l'armée du joueur", inline=False)
    embed.add_field(name='__MINEUR__:', value="Renvoie la valeur marchande de chaque mineurs du joueur\nLes prix des mineurs sont:\n__Mineur 1__: 70 yenis\n__Mineur 2__: 1000 yenis\n__Mineur 3__: 145 000 yenis\n__Mineur 4__: 4.6 millions de yenis\n__Mineur 5__: 1 milliard de yenis\n**Aucune réclamation sera écoutée.**", inline=False)
    embed.add_field(name='__RECRUTER__:', value="-> recruter <type> <nombre>\nPermet au joueur de former des troupes\nlorsqu'il est à sa base, il peut choisir parmi:\nChevaliers, Geants et Mages.", inline=False)
    embed.add_field(name='__CONSTRUIRE__:', value="-> construire <bâtiment>\nPermet la construction parmis les bâtiments suivant:\nMineur, Caserne...")
    embed.add_field(name='__SELL__:', value="-> sell <mine>\nVend les minerais de la mine correspondante\nau marchand du village\nPour choisir une des mines, le paramètre est: <mine+numero>\nSi le paramètre est <all>, vend tout\nSi le paramètre est <help>, précise les prix du marché.", inline=False)
    embed.add_field(name='__BUY__:', value="-> buy <objet> <type d'objet>\nPermet d'acheter un objet au village\nPour une capacité, la liste est détaille page 3", inline=False)

    embed.set_footer(text='Passer à la page 2 avec +help2', icon_url='https://cdn.discordapp.com/attachments/787678752812302336/788112921753944104/fleche_1.png')

    await ctx.send(embed=embed)

@client.command(aliases=['HELP2', 'Help2', 'aide2', 'AIDE2', 'Aide2', 'info2', 'INFO2', 'Info2', 'infos2', 'Infos2', 'INFOS2'])
async def help2(ctx):
    embed = discord.Embed(
        title='__REGLES SUR LES COMBATS__:',
        description='Si tu ne comprends toujours rien, mp moi, Apyre#6893',
        colour=discord.Color.orange()
    )

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name='__DUEL__:', value="-> duel <mise>\nLance une invitation à un duel à tout les joueurs,\nlorsque la personnes accepte avec 'rejoindre le combat', le duel commencera", inline=False)
    embed.add_field(name='REGLES SUR LES DUELS:', value="1) Ne pas envoyer de messages inutilement lorsque 2 personnes se battent,\n\n2) Chaque joueur possède 2 attaques, il a juste à inscrire le nom de celles-ci __SANS FAUTE__ pour les utiliser,\n\n3) Les efficacités sont:\nFEU --> sur AIR, AIR --> sur TERRE, TERRE --> sur EAU, EAU --> sur FEU\nElles multiplient les dégats par 2 et les inéfficacitées par 0,5. Vous avez 10% de chance de coup critique (x1.5 de dégats) et 7% de chance d'esquiver,\n\n4) Vous pouvez fuir le combat <fuite>, cela vous fait quand même perdre votre mise et peut vous apporter une malédiction")

    embed.set_footer(text='Passer à la page 3 avec +help3', icon_url='https://cdn.discordapp.com/attachments/787678752812302336/788112921753944104/fleche_1.png')
    await ctx.send(embed=embed)

@client.command(aliases=['HELP3', 'Help3', 'aide3', 'AIDE3', 'Aide3', 'info3', 'INFO3', 'Info3', 'infos3', 'Infos3', 'INFOS3'])
async def help3(ctx):
    embed = discord.Embed(
        title='__LISTE DES CAPACITÉES__:',
        description='Si tu ne comprends toujours rien, mp moi, Apyre#6893',
        colour=discord.Color.orange()
    )

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name='__AIR__', value="Lame d'air, 12 dégats, gratuit,\nVoltige, 10 dégats, gratuit,\nRush aerien, 21 dégats, 1000$,\nFlash Dash, 27 dégats, 53000$", inline=False)
    embed.add_field(name='__FEU__', value="Déflagration, 12 dégats, gratuit,\nBrasier, 10 dégats, gratuit,\nEruption cutannée, 22 dégats, 1200$,\nExplosion diabolique, 43 dégats, 150 000$", inline=False)
    embed.add_field(name='__EAU__', value="Bombe aquatique, 12 dégats, gratuit,\nTyphon, 11 dégats, grauit,\nAquajet, 20 dégats, 1200$,\nDéchainement marin, 32 dégats, 70 000$", inline=False)
    embed.add_field(name='__TERRE__', value="Fracture tectonique, 13 dégats, grauit,\nPoing de granite, 12 dégats, gratuit,\nEboulement d'acier, 23 dégats, 1450$,\nRafale tellurique, 35 dégats, 100 000$", inline=False)

    embed.set_footer(text='Passer à la page 4 avec +help4', icon_url='https://cdn.discordapp.com/attachments/787678752812302336/788112921753944104/fleche_1.png')

    await ctx.send(embed=embed)

@client.command()
async def clear(ctx, nombre):
    await ctx.channel.purge(limit=nombre)

@tasks.loop(seconds=30)
async def generer_monnaie():
    '''
    Mineur#1 Niveau1:5$
    Mineur#2 Niveau1:240$
    Mineur#3 Niveau1:12 000$
    Mineur#4 Niveau1:150 000$
    Mineur#5 Niveau1:1 200 000$
    '''

    connexion = sqlite3.connect('base_donnes_bot_discord.db')
    curseur = connexion.cursor()

    table_joueurs = curseur.execute('SELECT * from joueurs')
    liste_joueurs = table_joueurs.fetchall()

    table_mines = curseur.execute('SELECT * from mines')

    indice = 0

    for les_mines in table_mines.fetchall():
        if liste_joueurs[indice][4] <= 93:
            curseur.execute('UPDATE joueurs SET pv = ? WHERE pseudo = ?', (liste_joueurs[indice][4] + randint(1, 3), liste_joueurs[indice][0]))
        else:
            curseur.execute('UPDATE joueurs SET pv = ? WHERE pseudo = ?', (100, liste_joueurs[indice][0]))

        for i in range(5): #update mines

            if les_mines[i+1] != -1: #si le mineur fonctionne
                if i == 0: #mineur 1
                    curseur.execute('UPDATE mines SET mine1 = ? WHERE pseudo = ?', (les_mines[i+1] + 5, les_mines[0]))


                elif i == 1:
                    curseur.execute('UPDATE mines SET mine2 = ? WHERE pseudo = ?', (les_mines[i+1] + 240, les_mines[0]))

                elif i == 2:
                    curseur.execute('UPDATE mines SET mine3 = ? WHERE pseudo = ?',
                                    (les_mines[i + 1] + 12000, les_mines[0]))

                elif i == 3:
                    curseur.execute('UPDATE mines SET mine4 = ? WHERE pseudo = ?',
                                    (les_mines[i + 1] + 150000, les_mines[0]))

                elif i == 4:
                    curseur.execute('UPDATE mines SET mine5 = ? WHERE pseudo = ?',
                                    (les_mines[i + 1] + 1200000, les_mines[0]))
        indice += 1

        connexion.commit()
    connexion.close()

@client.command()
async def purger(ctx):
    channel = ctx.channel


@client.command()
async def testt(ctx):
    roleVer = 'bot test'  # role to add
    user = ctx.message.author  # user
    role = roleVer  # change the name from roleVer to role

    print("""Attempting to Verify {}""".format(user))
    try:
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))  # add the role
    except Exception as e:
        print(e)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('Nzg3Mjk3NDY1MTA2ODI1MjE3.X9S55g.Ux850YBoFcZUx35r6-ReBXYwxY0')#on utilise la clef et on lance le bot :p