import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import quickstart
import data
import asyncio
from discord import Color

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    load_dotenv('.env')
    TOKEN: str = os.getenv('Token')
    print(TOKEN)

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)




    @bot.command(name='opret_kamp')
    async def create_match(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        # Send initial message
        embed = discord.Embed(title='Hi plz read the following msg', description='Here are the help commands. To help with elustrating how the command should look like. \n'
                                                                                 'here is a eksampel. 15/05/2023 1 Randoms 2 L 3-12 2-4 1 1. \n'
                                                                                 'So it work be like this \n'
                                                                                 '[date] [Game_Type] [Opponets] [Map] [Win/Loss] [T-rounds] [CT-rounds] [T pistol] [CT pistol]')
        embed.add_field(name='Game type', value='1 = faceit \n 2 = scrim \n 3 = metal \n 4 = yousee \n 5 = power')
        embed.add_field(name='Map type', value='1 = Ancient \n 2 = Inferno \n 3 = Nuke \n 4 = Vertigo \n 5 = Overpass \n 6 = Mirage \n 7 = anubis')
        await ctx.send(embed=embed)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            i = 0
            while i == 0:
                # Wait for the user's response
                msg = await bot.wait_for('message', check=check, timeout=200)

                # Access the variables from the user's response
                variables = msg.content.split()

                if len(variables) >= 9:
                    variable1 = variables[0]
                    variable2 = data.game_type(int(variables[1]))
                    variable3 = variables[2]
                    variable4 = data.maps(int(variables[3]))
                    variable5 = variables[4]
                    variable6 = variables[5] #t side round
                    variable7 = variables[6] #ct side rounds
                    variable8 = int(variables[7])
                    variable9 = int(variables[8])

                    list1 = variable6.split('-')
                    list2 = variable7.split('-')

                    variable10 = int(list1[0])
                    variable11 = int(list1[1])
                    variable12 = int(list2[0])
                    variable13 = int(list2[1])
                    match_variables = [variable1, variable2, variable3, variable4, variable5, variable10, variable11, variable12, variable13, variable8, variable9]
                    # Call your function using the variables
                    # your_function(variable1, variable2)
                    embed = discord.Embed(title='These are the variables i got', description=f"Variables received: {variable1}, {variable2}, {variable3}, {variable4}, {variable5}, {variable6}, {variable7}, {variable8}, {variable9} \n"
                                                                                              f"If the values are correct type [yes], or if they are incorrect type [no]")
                    await ctx.send(embed=embed)
                    msg_check = await bot.wait_for('message', check=check)
                    if msg_check.content == 'yes' or msg_check.content == 'Yes':
                        x = 0
                        t = 0
                        while x == 0:
                            if val[2+t][0] == '' or val[2+t][0] == 'N/A':
                                print("hej")
                                quickstart.write_to_sheet(data.spread_id(channel_id), 'A'+str(3+t), 1+t)
                                for i in range(len(match_variables)):

                                    quickstart.write_to_sheet(data.spread_id(channel_id), data.match_stats(t)[i], match_variables[i])

                                x = 1
                                embed = discord.Embed(title='Match saved', description=f'The data have been processed. The match id is {1+t}')
                                await ctx.send(embed=embed)
                            else:
                                t = t + 1

                        i = 1
                    elif msg_check.content == 'no' or msg_check.content == 'No':
                        embed = discord.Embed(title='Data not processed', colour=0xe91e63, description='Plz try writing the values again')
                        await ctx.send(embed=embed)
                else:
                    await ctx.send("Please provide all of the values, before clicking enter")
        except asyncio.TimeoutError:
            await ctx.send("Timeout: Command cancelled.")

    @bot.tree.command(name='delete') #Der skal laves et fix hos stats'ne så faktisk alle statsne bliver slettet når denne command bruges.

    async def delete(interaction: discord.Interaction, match_id: int):
        channel = interaction.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))

        try:
            for i in range(match_id):
                if match_id == int(val[2+i][0]):
                    print("hej")

                    quickstart.write_to_sheet(data.spread_id(channel_id), 'A' + str(3 + match_id-1), 'N/A')
                    for i in range(11):
                        quickstart.write_to_sheet(data.spread_id(channel_id), data.match_stats(match_id-1)[i], 0)

        except:
            print("lort")



    @bot.tree.command(name='info', description='Displays all the commands you can use')
    async def info(interaction: discord.Interaction):
        embed = discord.Embed(title="Command List", description="Here are the available commands:")

        embed.add_field(name="/pistol", value="Displays all the pistol stats from your games")
        embed.add_field(name="!map_pistol", value="Displays the overall win% of pistol rounds for all maps")
        embed.add_field(name="!map_round", value="Displays the overall win% of rounds for all the maps")
        embed.add_field(name="!t_round", value="Displays the overall win% of rounds on t side")
        embed.add_field(name="!ct_round", value="Displays the overall win% of round is ct side")
        embed.add_field(name="/games", value="Displays the overall win% of your games")
        embed.add_field(name="!game_type", value="Displays the data of the game types u have played")
        embed.add_field(name="/stats [Name]", value="Displays the player data")
        embed.add_field(name="/match [Match id]", value="Displays the given match")
        embed.add_field(name="/stats_in [Name] [Match id] [kills] [assist] [deaths]", value="Saves player stats to the sheet")
        embed.add_field(name="!opret_kamp [date] [Game_Type] [Opponents] [Map] [Win/Loss] [T-rounds] [CT-rounds] [T pistol] [CT pistol]", value="Saves the data from a match. Dont type the data from the match at the same time as the command, type the command, then type the data.")

        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='pistol')
    async def pistol_overall(interaction: discord.Interaction):
        channel = interaction.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Overall pistol stats', description="This is all of your pistol stats", colour=15844367)

        embed.add_field(name='Overall pistol wins', value=f'You have won {val[20][20]} \n of your pistol rounds')
        embed.add_field(name='Overall pistol wins', value=f'You have won {val[20][21]} \n of your t pistol rounds')
        embed.add_field(name='Overall pistol wins', value=f'You have won {val[20][22]} \n of your ct pistol rounds')

        await interaction.response.send_message(embed=embed)

    @bot.command(name='test')
    async def test(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Test', description='hejsa')
        #await ctx.send(embed=embed)
        print(val[2][0])

    @bot.tree.command(name="stats_in")
    async def stats_in(interaction: discord.Interaction, name: str, match_id:  int, kills: int, assist: int, deaths: int):
        channel = interaction.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        own_stats = [kills, assist, deaths]
        placeNr = 0
        kor = ''
        match = ''
        if name == val[59][20]:
            placeNr = 1
            kor = 'y'
            match = 'u'

        elif name == val[59][26]:
            placeNr = 2
            kor = 'AE'
            match = 'aa'

        try:
            if val[62 + match_id][20] != None and name == val[59][20] or val[62 + match_id][26] != None and name == val[59][26]:
                error = discord.Embed(title='Error', colour=0xe91e63, description='Some of the cells have been filled out, check if the match id is correct')
                await interaction.response.send_message(embed=error)
        except:
            for i in range(len(data.stats_own(match_id, placeNr))):
                quickstart.write_to_sheet(data.spread_id(channel_id), data.stats_own(match_id, placeNr)[i], own_stats[i])
            quickstart.write_to_sheet(data.spread_id(channel_id), kor + str(62 + match_id), int(kills) / int(deaths))
            quickstart.write_to_sheet(data.spread_id(channel_id), match + str(62 + match_id), match_id)
            embed = discord.Embed(title='Stats inputet', colour=0x2ecc71, description=f'Your stats have been saved for match {match_id} :)')
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='match')
    async def match_show(interaction: discord.Interaction, match_id: int):
        channel = interaction.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        try:
            if int(val[match_id + 1][0]) == match_id:
                if str(val[match_id + 1][5]) == 'L':
                    match_status = 'loss'
                    color = 0xe74c3c

                else:
                    match_status = 'Win'
                    color = 0x2ecc71
                embed = discord.Embed(title=f'Match {match_id}', colour=color, description=f'This match was played on {val[match_id + 1][1]} \n'
                                                                         f'This match was a {val[match_id + 1][2]} match, and was against {val[match_id + 1][3]} \n'
                                                                         f'The match was played on {val[match_id + 1][4]} and it was a total {match_status} \n'
                                                                         f'The match result was {int(val[match_id + 1][6]) + int(val[match_id + 1][9])}-{int(val[match_id + 1][7]) + int(val[match_id + 1][10])} \n')
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title='Error', colour=0xe91e63, description=f'Could not find the match with the given id  {match_id} {val[match_id + 1][0]}')
                await interaction.response.send_message(embed=embed)
        except:
            embed = discord.Embed(title='Error', colour=0xe91e63, description='Some of the cells have not been filled out, plz check agian')
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='stats')
    async def stats(interaction: discord.Interaction, name: str):
        channel = interaction.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))

        add = 0
        ig = ''
        if name == val[59][20]:
            add = 0
            ig = val[59][20]+"'s"

        elif name == val[59][26]:
            add = 3
            ig = val[59][26]+"'s"

        embed = discord.Embed(title='Player stats', description=f'Hi, {interaction.user.mention} This is {ig} stats from all of his matches :) \n \n'
                       f'Your AVG kills are [{val[36][26+add]}] \n \n'
                       f'Your AVG aissist are [{val[37][26+add]}] \n \n'
                       f'Your AVG deaths are [{val[38][26+add]}] \n \n'
                       f'Your din K/D are [{val[39][26+add]}]', colour=Color.purple())

        await interaction.response.send_message(embed=embed)

    @bot.command(name='map_pistol')
    async def pistol_maps(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Pistols on all maps', description=f'This is all data from your pistols\n '
                        f'Ancient Overall win% [{val[25][20]}] T side win% [{val[25][21]}] CT side win% [{val[25][22]}] \n'
                        f'Inferno Overall win% [{val[26][20]}] T side win% [{val[26][21]}] CT side win% [{val[26][22]}] \n'
                        f'Nuke Overall win% [{val[27][20]}] T side win% [{val[27][21]}] CT side win% [{val[27][22]}] \n'
                        f'Vertigo Overall win% [{val[28][20]}] T side win% [{val[28][21]}] CT side win% [{val[28][22]}] \n'
                        f'Overpass Overall win% [{val[29][20]}] T side win% [{val[29][21]}] CT side win% [{val[29][22]}] \n'
                        f'Mirage Overall win% [{val[30][20]}] T side win% [{val[30][21]}] CT side win% [{val[30][22]}] \n'
                        f'Anubis Overall win% [{val[31][20]}] T side win% [{val[31][21]}] CT side win% [{val[31 ][22]}]', colour=Color.purple())
        await ctx.send(embed=embed)

    @bot.command(name='map_round')
    async def round_maps(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Wins on all the maps', description=f'This is all data from your rounds on all maps\n \n'
                        f'Ancient Overall win% {val[19][26]} T side win% {val[19][27]} CT side win% {val[19][28]} \n \n'
                        f'Inferno Overall win% {val[20][26]} T side win% {val[20][27]} CT side win% {val[20][28]} \n \n'
                        f'Nuke Overall win% {val[21][26]} T side win% {val[21][27]} CT side win% {val[21][28]} \n \n'
                        f'Vertigo Overall win% {val[22][26]} T side win% {val[22][27]} CT side win% {val[22][28]} \n \n'
                        f'Overpass Overall win% {val[23][26]} T side win% {val[23][27]} CT side win% {val[23][28]} \n \n'
                        f'Mirage Overall win% {val[24][26]} T side win% {val[24][27]} CT side win% {val[24][28]} \n \n'
                        f'Anubis Overall win% {val[25][26]} T side win% {val[25][27]} CT side win% {val[25][28]}', colour=Color.purple())
        await ctx.send(embed=embed)

    @bot.command(name='t_round')
    async def t_round(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='T side rounds', description=f'This is the overall round win% for t side[{val[29][25]}]')
        await ctx.send(embed=embed)

    @bot.command(name='ct_round')
    async def ct_round(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='CT side rounds', description=f'This is the overall round win% for ct side[{val[29][26]}]')
        await ctx.send(embed=embed)

    @bot.tree.command(name='games')
    async def game(interaction: discord.Interaction):
        channel = interaction.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Overall games', description=f'You have played a total of [{val[26][31]}] games \n'
                        f'You have won a total of [{val[26][32]}] games \n'
                        f'You have lost a total of [{val[26][33]}] games \n'
                        f'You have a  win to loss ration of [{val[26][34]}]')

        await interaction.response.send_message(embed=embed)

    @bot.command(name='game_type')
    async def game_type(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Game types you played', description=f'You have played a total of [{val[37][20]}] Faceit games, and u have won a total of [{val[37][21]}]\n' 
                       f'You have played a total of [{val[38][20]}] Scrim games, and u have won a total of [{val[38][21]}]\n'
                       f'You have played a total of [{val[39][20]}] Metal games, and u have won a total of [{val[39][21]}]\n'
                       f'You have played a total of [{val[40][20]}] Yousee games, and u have won a total of [{val[40][21]}]\n'
                       f'You have played a total of [{val[41][20]}] Power games, and u have won a total of [{val[41][21]}]\n')
        await ctx.send(embed=embed)

    bot.run(TOKEN)
