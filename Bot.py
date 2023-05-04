import discord
from discord.ext import commands
from dotenv import load_dotenv
import quickstart
import data

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    t = data.func()

    TOKEN = 'Discord_Token'

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

        await ctx.send(embed=embed)

    @bot.command(name='pistol')
    async def pistolOverall(ctx):
        await ctx.send(t.overall_pistol_win)

    @bot.command(name='t_pistol')
    async def pistol_t_side(ctx):
        await ctx.send(t.t_side_pistol_win)

    @bot.command(name='ct_pistol')
    async def pistol_ct_side(ctx):
        await ctx.send(t.ct_side_pistol_win,)


    #TODO lav det om så der ikke bliver sendt 8 enkelt beskeder men som en samlet.


    @bot.command(name='map_pistol')
    async def pistol_maps(ctx):
        await ctx.send(f'This is all data from your pistols\n '
                        f'Ancient Overall win% [{t.ancient_pistol_overall[0]}] T side win% [{t.ancient_pistol_overall[1]}] CT side win% [{t.ancient_pistol_overall[2]}] \n'
                        f'Inferno Overall win% [{t.inferno_pistol_overall[0]}] T side win% [{t.inferno_pistol_overall[1]}] CT side win% [{t.inferno_pistol_overall[2]}] \n'
                        f'Nuke Overall win% [{t.nuke_pistol_overall[0]}] T side win% [{t.nuke_pistol_overall[1]}] CT side win% [{t.nuke_pistol_overall[2]}] \n'
                        f'Vertigo Overall win% [{t.vertigo_pistol_overall[0]}] T side win% [{t.vertigo_pistol_overall[1]}] CT side win% [{t.vertigo_pistol_overall[2]}] \n'
                        f'Overpass Overall win% [{t.overpass_pistol_overall[0]}] T side win% [{t.overpass_pistol_overall[1]}] CT side win% [{t.overpass_pistol_overall[2]}] \n'
                        f'Mirage Overall win% [{t.mirage_pistol_overall[0]}] T side win% [{t.mirage_pistol_overall[1]}] CT side win% [{t.mirage_pistol_overall[2]}] \n'
                        f'Anubis Overall win% [{t.anubis_pistol_overall[0]}] T side win% [{t.anubis_pistol_overall[1]}] CT side win% [{t.anubis_pistol_overall[2]}]')

    @bot.command(name='map_round')
    async def round_maps(ctx):
        await ctx.send(f'This is all data from your rounds on all maps\n'
                        f'Ancient Overall win% [{t.ancient_round_overall[0]}] T side win% [{t.ancient_round_overall[1]}] CT side win% [{t.ancient_round_overall[2]}] \n'
                        f'Inferno Overall win% [{t.inferno_round_overall[0]}] T side win% [{t.inferno_round_overall[1]}] CT side win% [{t.inferno_round_overall[2]}] \n'
                        f'Nuke Overall win% [{t.nuke_round_overall[0]}] T side win% [{t.nuke_round_overall[1]}] CT side win% [{t.nuke_round_overall[2]}] \n'
                        f'Vertigo Overall win% [{t.vertigo_round_overall[0]}] T side win% [{t.vertigo_round_overall[1]}] CT side win% [{t.vertigo_round_overall[2]}] \n'
                        f'Overpass Overall win% [{t.overpass_round_overall[0]}] T side win% [{t.overpass_round_overall[1]}] CT side win% [{t.overpass_round_overall[2]}] \n'
                        f'Mirage Overall win% [{t.mirage_round_overall[0]}] T side win% [{t.mirage_round_overall[1]}] CT side win% [{t.mirage_round_overall[2]}] \n'
                        f'Anubis Overall win% [{t.anubis_round_overall[0]}] T side win% [{t.anubis_round_overall[1]}] CT side win% [{t.anubis_round_overall[2]}]')

    @bot.command(name='t_round')
    async def t_round(ctx):
        await ctx.send(f'This is the overall round win% for t side[{t.t_side_round_overall}]')

    @bot.command(name='ct_round')
    async def ct_round(ctx):
        await ctx.send(f'This is the overall round win% for t side[{t.ct_side_round_overall}]')

    @bot.command(name='games')
    async def game(ctx):
        await ctx.send(f'You have played a total of [{t.games}] games \n'
                        f'You have won a total of [{t.game_wins}] games \n'
                        f'You have lost a total of [{t.game_loss}] games \n'
                        f'You have a  win to loss ration of [{t.game_win_pro}]')

    bot.run(TOKEN)
