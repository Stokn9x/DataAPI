import discord
from discord.ext import commands
from dotenv import load_dotenv
import quickstart
import data

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    TOKEN = 'MTEwMzI3NTMzNTcxMTIwMzM4OQ.GUZTm6.26ZHc0dHBOk6z_9wPKq6yAqFdPCmRpRxbX5hJY'

    bot = commands.Bot(command_prefix="!", intents=intents)



    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        channel = bot.get_channel(1103348691466723399)
        #await channel.send(f'{bot.user} is now updated!')


    @bot.command(name='info')
    async def infoo(ctx):
        embed = discord.Embed(title="Command List", description="Here are the available commands:")

        embed.add_field(name="!pistol", value="Displays the overall win% of pistol rounds")
        embed.add_field(name="!t_pistol", value="Displays the overall win% of pistol rounds for t side")
        embed.add_field(name="!ct_pistol", value="Displays the overall win% of pistol rounds for ct side")
        embed.add_field(name="!map_pistol", value="Displays the overall win% of pistol rounds for all maps")
        embed.add_field(name="!map_round", value="Displays the overall win% of rounds for all the maps")
        embed.add_field(name="!t_round", value="Displays the overall win% of rounds on t side")
        embed.add_field(name="!ct_round", value="Displays the overall win% of round is ct side")
        embed.add_field(name="!games", value="Displays the overall win% of your games")

        await ctx.send(embed=embed)

    @bot.command(name='pistol')
    async def pistolOverall(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(val[20][20])

    @bot.command(name='test')
    async def test(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(val[20][20])

    @bot.command(name='t_pistol')
    async def pistol_t_side(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(val[20][21])

    @bot.command(name='ct_pistol')
    async def pistol_ct_side(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(val[20][22])


    #TODO lav det om så der ikke bliver sendt 8 enkelt beskeder men som en samlet.


    @bot.command(name='map_pistol')
    async def pistol_maps(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(f'This is all data from your pistols\n '
                        f'Ancient Overall win% [{val[25][20]}] T side win% [{val[25][21]}] CT side win% [{val[25][22]}] \n'
                        f'Inferno Overall win% [{val[26][20]}] T side win% [{val[26][21]}] CT side win% [{val[26][22]}] \n'
                        f'Nuke Overall win% [{val[27][20]}] T side win% [{val[27][21]}] CT side win% [{val[27][22]}] \n'
                        f'Vertigo Overall win% [{val[28][20]}] T side win% [{val[28][21]}] CT side win% [{val[28][22]}] \n'
                        f'Overpass Overall win% [{val[29][20]}] T side win% [{val[29][21]}] CT side win% [{val[29][22]}] \n'
                        f'Mirage Overall win% [{val[30][20]}] T side win% [{val[30][21]}] CT side win% [{val[30][22]}] \n'
                        f'Anubis Overall win% [{val[31][20]}] T side win% [{val[31][21]}] CT side win% [{val[31 ][22]}]')

    @bot.command(name='map_round')
    async def round_maps(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(f'This is all data from your rounds on all maps\n'
                        f'Ancient Overall win% [{val[19][26]}] T side win% [{val[19][27]}] CT side win% [{val[19][28]}] \n'
                        f'Inferno Overall win% [{val[20][26]}] T side win% [{val[20][27]}] CT side win% [{val[20][28]}] \n'
                        f'Nuke Overall win% [{val[21][26]}] T side win% [{val[21][27]}] CT side win% [{val[21][28]}] \n'
                        f'Vertigo Overall win% [{val[22][26]}] T side win% [{val[22][27]}] CT side win% [{val[22][28]}] \n'
                        f'Overpass Overall win% [{val[23][26]}] T side win% [{val[23][27]}] CT side win% [{val[23][28]}] \n'
                        f'Mirage Overall win% [{val[24][26]}] T side win% [{val[24][27]}] CT side win% [{val[24][28]}] \n'
                        f'Anubis Overall win% [{val[25][26]}] T side win% [{val[25][27]}] CT side win% [{val[25][28]}]')

    @bot.command(name='t_round')
    async def t_round(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(f'This is the overall round win% for t side[{val[29][25]}]')

    @bot.command(name='ct_round')
    async def ct_round(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(f'This is the overall round win% for t side[{val[29][26]}]')

    @bot.command(name='games')
    async def game(ctx):
        val = quickstart.connect_to_sheet()
        await ctx.send(f'You have played a total of [{val[26][31]}] games \n'
                        f'You have won a total of [{val[26][32]}] games \n'
                        f'You have lost a total of [{val[26][33]}] games \n'
                        f'You have a  win to loss ration of [{val[26][34]}]')

    bot.run(TOKEN)
