
def spread_id(channel_id):
    try:
        if channel_id == 1107565551766745139: #Zer0
            return '1l2aXE0Lu3vcOXoFXKyiN6xrpofRsJrKyZpSHHFUNGOg'

        elif channel_id == 1107565600647172146: #K1ngWave
            return '11hUQnDVInBjS744s842yVJCPYeDpyymg79CgLrfPshE'

        elif channel_id == 1107566039014838302: #Monner
            return '1CL7DL68aB9VjI94f3g33kJ7W9wzGDE8YsruW2g9kLAQ'

        elif channel_id == 1107573013651660820: #AB
            return '1IRv0QicOU044COgTk0ACK__u8EjOhim3lnfRZthdlaM'

        elif channel_id == 1103348691466723399: #Cepter
            return '1HuKfTI0KKPvdlxY5MX9BIzlSExS2kLzJ7BdW739vbKQ'

    except:
        print("channel not working")

def stats_own(id):
    a = 'V'
    b = 'W'
    c = 'X'
    list = [a+str(62+id), b+str(62+id), c+str(62+id)]

    return list

def match_stats(id):
    a = 'B'
    b = 'C'
    c = 'D'
    d = 'E'
    e = 'F'
    f = 'G'
    g = 'H'
    h = 'J'
    j = 'K'
    k = 'O'
    o = 'P'
    match_list = [a+str(3+id), b+str(3+id), c+str(3+id), d+str(3+id), e+str(3+id), f+str(3+id), g+str(3+id), h+str(3+id), j+str(3+id), k+str(3+id), o+str(3+id)]
    return match_list


def maps(map):
    if map == 1:
        return 'Ancient'
    elif map == 2:
        return 'Inferno'
    elif map == 3:
        return 'Nuke'
    elif map == 4:
        return 'Vertigo'
    elif map == 5:
        return 'Overpass'
    elif map == 6:
        return 'Mirage'
    elif map == 7:
        return 'Anubis'
