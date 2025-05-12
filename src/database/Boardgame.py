import src.database.connect as data#connact
from psycopg2 import sql#/.        ./

class Boardgame(object) :# Gameboard
    def __init__(self, id, name, min_players, max_players, playing_time, complexity):
        self.id = id
        self.name = name
        self.min_players = min_players
        self.max_players = max_players
        self.playing_time = playing_time
        self.complexity = complexity


def load(id: int):#self, .
    connect = data.connect()
    cursor = connect.cursor()#data
    cursor.execute("SELECT (game_name, min_players, max_players, playing_time, complexity) FROM games WHERE id = %s", (id, ))# games_id
    res = cursor.fetchone()# qursor
    return Boardgame(id, res[0], res[1], res[2], res[3], res[4])# Gameboard()


def pattern_search(pattern: str):#self, .
    connect = data.connect()
    cursor = connect.cursor()
    query = sql.SQL("SELECT * FROM games WHERE games_name LIKE {pattern};").format(
        pattern=sql.Literal(("%" + pattern + "%")))# str(command.args))  games_name
    cursor.execute(query)
    query_result = cursor.fetchall()#(9())((((()))))
    result = []
    for game in query_result : # rel i
        result.append(Boardgame(game[0], game[1], game[2], game[3], game[4], game[5]))
    return result
    #staticmethod(load)
    #staticmethod(pattern_search)#patterb