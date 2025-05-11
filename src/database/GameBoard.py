import database.connect as data
from psycopg2 import Error


class GameBoard : #()
  def __init__(self, id, name, min_players, max_players, playing_time, complexity):
    self.id = id
    self.name = name
    self.min_players = min_players
    self.max_players = max_players
    self.playing_time = playing_time
    self.complexity = complexity
    print(self.name)


def load(id: int):
    connect = data.connect()
    cursor = connect.cursor()  # data
    cursor.execute("SELECT * FROM types_boardgames WHERE id = %s",
                   (id,))
    res = cursor.fetchone()
    #print(res)
    return GameBoard(id, res[1], res[2], res[3], res[4], res[5])


def find(name: str):
  find_query = """
  SELECT id, name
  FROM types_boardgames 
  WHERE name ILIKE %s
  """ 
  search_pattern = f"%{name}%"


  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(find_query,(search_pattern, ))
  answer = cursor.fetchall()
  return answer

def return_game(id: int) :
    connect = data.connect()
    cursor = connect.cursor()
    try :
        cursor.execute("UPDATE boardgames SET took_user_id = NULL WHERE id = %s ;", (id, ))#
        connect.commit()
        return True
    except Error as e :
        print(e.pgerror)
        return False
