import quickstart
class Data:
    def __init__(self):
        val =quickstart.connect_to_sheet()
        #Enkelt celle pstol data
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

        #enkelt celle game wins / losses
        self.games = val[26][29]
        self.game_wins = val[26][30]
        self.game_loss = val[26][31]
        self.game_win_pro = val[26][32]


def func():
    return Data()