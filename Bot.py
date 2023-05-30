import discord
from discord.ext import commands
from dotenv import load_dotenv
import quickstart
import data
import asyncio


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    TOKEN = 'MTEwMzI3NTMzNTcxMTIwMzM4OQ.G_HaDh.oCoZbYiANChGQ_upyzZiibsRIlX8MVJ37AMaiAGG'

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
    async def opret(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        # Send initial message
        embed = discord.Embed(title='Hi plz read the following msg', description='Here are the help commands. To help with elustrating how the command should look like. \n'
                                                                                 'here is a eksampel. 15/05/2023 1 randoms 2 L 3-12 2-4 1 1. \n'
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
                msg = await bot.wait_for('message', check=check, timeout=60)

                # Access the variables from the user's response
                variables = msg.content.split()

                if len(variables) >= 9:
                    variable1 = variables[0]
                    variable2 = variables[1]
                    variable3 = variables[2]
                    variable4 = variables[3] # map convert
                    variable4 = data.maps(variables[3])
                    variable5 = variables[4]
                    variable6 = variables[5] #
                    variable7 = variables[6] #
                    variable8 = variables[7]
                    variable9 = variables[8]

                    list1 = variable6.split('-')
                    list2 = variable7.split('-')

                    variable10 = list1[0]
                    variable11 = list1[1]
                    variable12 = list2[0]
                    variable13 = list2[1]
                    match_stats = [variable1, variable2, variable3, variable4, variable5, variable10, variable11, variable12, variable13, variable8, variable9]
                    # Call your function using the variables
                    # your_function(variable1, variable2)
                    embed = discord.Embed(title='Thesse are the variables i got', description=f"Variables received: {variable1}, {variable2}, {variable3}, {variable4}, {variable5}, {variable6}, {variable7}, {variable8}, {variable9} \n"
                                                                                              f"If the valuse are correct type [yes], or if they are incorrect type [no]")
                    await ctx.send(embed=embed)
                    msg_check = await bot.wait_for('message', check=check)
                    if msg_check.content == 'yes' or msg_check.content == 'Yes':
                        embed = discord.Embed(title='Match saved', description='The data have been processed.')
                        await ctx.send(embed=embed)
                        x = 0
                        t = 0
                        while x == 0:
                            if int(val[2+t][0]) != t + 1: #Dette virker ikke skal laves om
                                print("hej")
                                quickstart.write_to_sheet(data.spread_id(channel_id), 'A'+str(3+t), 3+t)
                                for i in range(len(match_stats)):

                                    quickstart.write_to_sheet(data.spread_id(channel_id), data.match_stats(t)[i],match_stats[i])

                                x = 1

                            else:
                                t = t + 1

                        i = 1
                    elif msg_check.content == 'no' or msg_check.content == 'No':
                        embed = discord.Embed(title='Data not processed', colour=0xe91e63,description='Plz try writing the values again')
                        await ctx.send(embed=embed)
                else:
                    await ctx.send("Please provide all of the values, before clicking enter")
        except asyncio.TimeoutError:
            await ctx.send("Timeout: Command cancelled.")


    @bot.tree.command(name='info', description='Displays all the commands you can use')
    async def info(interaction: discord.Interaction):
        embed = discord.Embed(title="Command List", description="Here are the available commands:")

        embed.add_field(name="!pistol", value="Displays the overall win% of pistol rounds")
        embed.add_field(name="!t_pistol", value="Displays the overall win% of pistol rounds for t side")
        embed.add_field(name="!ct_pistol", value="Displays the overall win% of pistol rounds for ct side")
        embed.add_field(name="!map_pistol", value="Displays the overall win% of pistol rounds for all maps")
        embed.add_field(name="!map_round", value="Displays the overall win% of rounds for all the maps")
        embed.add_field(name="!t_round", value="Displays the overall win% of rounds on t side")
        embed.add_field(name="!ct_round", value="Displays the overall win% of round is ct side")
        embed.add_field(name="!games", value="Displays the overall win% of your games")
        embed.add_field(name="!game_type", value="Displays the data of the game types u have played")
        embed.add_field(name="!stats", value="Displays the player data")
        embed.add_field(name="!match [Match id]", value="Displays the given match")
        embed.add_field(name="!stats_in [Match id] [kills] [assist] [deaths]", value="Saves player stats to the sheet")

        await interaction.response.send_message(embed=embed)

    @bot.command(name='pistol')
    async def pistolOverall(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Overall pistol wins', description=f'You have won [{val[20][20]}] of your pistol rounds')
        await ctx.send(embed=embed)

    @bot.command(name='test')
    async def test(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Test', description='hejsa')
        #await ctx.send(embed=embed)
        print(val[2][0])

    @bot.command(name="stats_in")
    async def stats_in(ctx, id:  int, arg1: int, arg2: int, arg3: int):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        own_stats = [arg1,arg2,arg3]
        try:
            if int(val[62 + (id)][21]) != None or int(val[62 + (id)][22]) != None or int(val[62 + (id)][23]) != None:
                embed = discord.Embed(title='Error', colour=0xe91e63,description='Some of the cells have been filled out, check if the match id is correct')
                await ctx.send(embed=embed)
        except:
            for i in range(len(data.stats_own(id))):
                quickstart.write_to_sheet(data.spread_id(channel_id), data.stats_own(id)[i], own_stats[i])
            quickstart.write_to_sheet(data.spread_id(channel_id), 'y'+str(62+id), int(arg1) / int(arg3))
            embed = discord.Embed(title='Stats inputet', colour=0x2ecc71, description=f'Your stats have been saved for match [{id}] :)')
            await ctx.send(embed=embed)

    @bot.command(name='match')
    async def match_show(ctx, arg1: int):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        try:
            if int(val[arg1+1][0]) == arg1:
                if str(val[arg1+1][5]) == 'L':
                    match_status = 'loss'
                    color = 0xe74c3c

                else:
                    match_status = 'Win'
                    color = 0x2ecc71
                embed = discord.Embed(title=f'Match {arg1}', colour=color, description=f'This match was played on {val[arg1+1][1]} \n'
                                                                         f'This match was a {val[arg1+1][2]} and was aginst {val[arg1+1][3]} \n'
                                                                         f'The match was played on {val[arg1+1][4]} and it was a total {match_status} \n'
                                                                         f'The match result was {int(val[arg1+1][6]) + int(val[arg1+1][9])}-{int(val[arg1+1][7]) + int(val[arg1+1][10])} \n')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Error', colour=0xe91e63, description=f'Could not find the match with the given id  {arg1} {val[arg1+1][0]}')
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title='Error', colour=0xe91e63, description='Some of the cells have not been filled out, plz check agian')
            await ctx.send(embed=embed)


    @bot.command(name='stats')
    async def stats(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        author = ctx.author
        embed = discord.Embed(title='Player stats', description=f'Hi, {author.mention} nu skal du bare høre hvordan du har klaret dig \n'
                       f'Din AVG kills er [{val[36][26]}] \n'
                       f'Din AVG aissist er [{val[37][26]}] \n'
                       f'Din AVG deaths er [{val[38][26]}] \n'
                       f'og din K/D er [{val[39][26]}]')
        await ctx.send(embed=embed)
    @bot.command(name='t_pistol')
    async def pistol_t_side(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='T side pistol', description=f'You have won [{val[20][21]}] of your t pistols')
        await ctx.send(embed=embed)

    @bot.command(name='ct_pistol')
    async def pistol_ct_side(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='CT side pistol', description=f'You have won [{val[20][22]}] of your ct pistols')
        await ctx.send(embed=embed)


    #TODO lav det om så der ikke bliver sendt 8 enkelt beskeder men som en samlet.


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
                        f'Anubis Overall win% [{val[31][20]}] T side win% [{val[31][21]}] CT side win% [{val[31 ][22]}]')
        await ctx.send(embed=embed)

    @bot.command(name='map_round')
    async def round_maps(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Wins on all the maps', description=f'This is all data from your rounds on all maps\n'
                        f'Ancient Overall win% [{val[19][26]}] T side win% [{val[19][27]}] CT side win% [{val[19][28]}] \n'
                        f'Inferno Overall win% [{val[20][26]}] T side win% [{val[20][27]}] CT side win% [{val[20][28]}] \n'
                        f'Nuke Overall win% [{val[21][26]}] T side win% [{val[21][27]}] CT side win% [{val[21][28]}] \n'
                        f'Vertigo Overall win% [{val[22][26]}] T side win% [{val[22][27]}] CT side win% [{val[22][28]}] \n'
                        f'Overpass Overall win% [{val[23][26]}] T side win% [{val[23][27]}] CT side win% [{val[23][28]}] \n'
                        f'Mirage Overall win% [{val[24][26]}] T side win% [{val[24][27]}] CT side win% [{val[24][28]}] \n'
                        f'Anubis Overall win% [{val[25][26]}] T side win% [{val[25][27]}] CT side win% [{val[25][28]}]')
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

    @bot.command(name='games')
    async def game(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Overall games', description=f'You have played a total of [{val[26][31]}] games \n'
                        f'You have won a total of [{val[26][32]}] games \n'
                        f'You have lost a total of [{val[26][33]}] games \n'
                        f'You have a  win to loss ration of [{val[26][34]}]')
        await ctx.send(embed=embed)

    @bot.command(name='game_type')
    async def game_type(ctx):
        channel = ctx.channel
        channel_id = channel.id
        val = quickstart.connect_to_sheet(data.spread_id(channel_id))
        embed = discord.Embed(title='Game types you played', description=f'You have played a total of [{val[37][20]}] faceit games, and u have won a total of [{val[37][21]}]\n' 
                       f'You have played a total of [{val[38][20]}] scrim games, and u have won a total of [{val[38][21]}]\n'
                       f'You have played a total of [{val[39][20]}] metal games, and u have won a total of [{val[39][21]}]\n'
                       f'You have played a total of [{val[40][20]}] yousee games, and u have won a total of [{val[40][21]}]\n'
                       f'You have played a total of [{val[41][20]}] power games, and u have won a total of [{val[41][21]}]\n')
        await ctx.send(embed=embed)



    bot.run(TOKEN)
