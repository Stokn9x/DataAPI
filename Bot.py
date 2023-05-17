import discord
from discord.ext import commands
from dotenv import load_dotenv
import quickstart
import data


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    TOKEN = 'MTEwMzI3NTMzNTcxMTIwMzM4OQ.G_HaDh.oCoZbYiANChGQ_upyzZiibsRIlX8MVJ37AMaiAGGG'

    bot = commands.Bot(command_prefix="!", intents=intents)


    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)

    @bot.tree.command(name='hej')
    async def hi(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! this is a slash command")

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
        await ctx.send(embed=embed)
        print(val[2][0])

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
