import database.connect as data


class TypeBoardgame:
  def __init__(
    self, 
    id, 
    name, 
    min_players:int, 
    max_players:int, 
    playing_time, 
    complexity
  ):
    self.id = id
    self.name = name
    self.min_players = min_players
    self.max_players = max_players
    self.playing_time = playing_time
    self.complexity = complexity


def load_by_id(id: int):
  connect = data.connect()
  cursor = connect.cursor()
  cursor.execute("""
  SELECT * 
  FROM types_boardgames 
  WHERE id = %s""",
  (id,))
  res = cursor.fetchone()
  return GameBoard(
    id, 
    res[1], 
    int(res[2]), 
    int(res[3]), 
    res[4], 
    res[5]
  )