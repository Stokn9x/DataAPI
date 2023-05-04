from __future__ import print_function

import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import discord
from discord.ext import commands
from dotenv import load_dotenv
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1GmCP7PStzszbd31zNKqcVqv_QuN12LbI0UzJjNvl05M'
SAMPLE_RANGE_NAME = 'Results'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


def connect_to_sheet():
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values


class Data:
    def __init__(self):
        val = connect_to_sheet()
        #Enkelt celle pistol data
        self.overall_pistol_win = val[20][18]
        self.t_side_pistol_win = val[20][19]
        self.ct_side_pistol_win = val[20][20]

        #Multi celle pistol data
        self.ancient_pistol_overall = [val[25][18], val[25][19], val[25][20]]
        self.inferno_pistol_overall = [val[26][18], val[26][19], val[26][20]]
        self.nuke_pistol_overall = [val[27][18], val[27][19], val[27][20]]
        self.vertigo_pistol_overall = [val[28][18], val[28][19], val[28][20]]
        self.overpass_pistol_overall = [val[29][18], val[29][19], val[29][20]]
        self.mirage_pistol_overall = [val[30][18], val[30][19], val[30][20]]
        self.anubis_pistol_overall = [val[31][18], val[31][19], val[31][20]]

        #Multi celle pistol data
        self.ancient_round_overall = [val[19][24], val[19][25], val[19][26]]
        self.inferno_round_overall = [val[20][24], val[20][25], val[20][26]]
        self.nuke_round_overall = [val[21][24], val[21][25], val[21][26]]
        self.vertigo_round_overall = [val[22][24], val[22][25], val[22][26]]
        self.overpass_round_overall = [val[23][24], val[23][25], val[23][26]]
        self.mirage_round_overall = [val[24][24], val[24][25], val[24][26]]
        self.anubis_round_overall = [val[25][24], val[25][25], val[25][26]]

        #enkelt celle t / ct win
        self.t_side_round_overall = val[29][23]
        self.ct_side_round_overall = val[29][24]


def func():
    return Data()


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    t = func()

    TOKEN = 'Discord_Token'

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.command(name='pistol')
    async def pistolOverall(ctx):
        await ctx.send(t.overall_pistol_win)

    @bot.command(name='t_pistol')
    async def pistol_t_side(ctx):
        await ctx.send(t.t_side_pistol_win)

    @bot.command(name='ct_pistol')
    async def pistol_ct_side(ctx):
        await ctx.send(t.ct_side_pistol_win,)

    @bot.command(name='map_pistol')
    async def pistol_maps(ctx):
        await ctx.send(f'Ancient Overall win% [{t.ancient_pistol_overall[0]}] T side win% [{t.ancient_round_overall[1]}] CT side win% [{t.ancient_pistol_overall[2]}]')
        await ctx.send(f'Inferno Overall win% [{t.inferno_pistol_overall[0]}] T side win% [{t.inferno_pistol_overall[1]}] CT side win% [{t.inferno_pistol_overall[2]}]')
        await ctx.send(f'Nuke Overall win% [{t.nuke_pistol_overall[0]}] T side win% [{t.nuke_pistol_overall[1]}] CT side win% [{t.nuke_pistol_overall[2]}]')
        #await ctx.send('Vertigo Overall win%', t.vertigo_pistol_overall[0],'T side win%', t.vertigo_pistol_overall[1],'CT side win%', t.vertigo_pistol_overall[2])
        #await ctx.send('Overpass Overall win%', t.overpass_pistol_overall[0],'T side win%', t.overall_pistol_win[1],'CT side win%', t.overpass_pistol_overall[2])
        #await ctx.send('Mirage Overall win%', t.mirage_pistol_overall[0],'T side win%', t.mirage_pistol_overall[1],'CT side win%', t.mirage_pistol_overall[2])
        #await ctx.send('Anubis Overall win%', t.anubis_pistol_overall[0],'T side win%', t.anubis_pistol_overall[1],'CT side win%', t.anubis_pistol_overall[2])

    bot.run(TOKEN)




