import database.connect as data


class TypeBoardgame:
  def __init__(
    self, 
    id:int, 
    name, 
    min_players:int, 
    max_players:int, 
    min_playing_time:int, 
    max_playing_time:int, 
    age:int,
    image_url
  ):
    self.id = id
    self.name = name
    self.min_players = min_players
    self.max_players = max_players
    self.min_playing_time = min_playing_time
    self.max_playing_time = max_playing_time
    self.age = age
    self.image_url = image_url
  
  def playing_time(self):
    if self.max_playing_time > 999:
      return f"{self.min_playing_time}+"
    if self.max_playing_time == self.min_playing_time:
      return f"{self.min_playing_time}"
    return f"{self.min_playing_time}-{self.max_playing_time}"
    


def load_by_id(id: int):
  connect = data.connect()
  cursor = connect.cursor()
  cursor.execute("""
  SELECT * 
  FROM types_boardgames 
  WHERE id = %s""",
  (id,))
  res = cursor.fetchone()
  return TypeBoardgame(
    id, 
    res[1], 
    int(res[2]), 
    int(res[3]), 
    int(res[4]),
    int(res[5]),
    int(res[6]),
    res[7]
  )


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