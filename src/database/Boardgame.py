import database.connect as data

class Boardgame(object):
  def __init__(
    self, 
    id:int,
    owner_user_id:int,
    type_boardgame_id:int,
    took_user_id,
    is_bought,
    name
  ):
    self.id = id
    self.name = name
    self.owner_user_id = owner_user_id
    self.type_boardgame_id = type_boardgame_id
    self.took_user_id = took_user_id
    self.is_bought = is_bought

  def delete(self):
    delete_query = """
    DELETE FROM boardgames
    WHERE id = %s
    """
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(delete_query,(self.id, ))
    
    connect.commit()

def load_by_id(id: int):
  select_query = """
  SELECT bg.*, tbg.name
  FROM boardgames bg
  JOIN types_boardgames tbg 
  ON bg.type_boardgame_id = tbg.id
  WHERE bg.id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()
  cursor.execute(select_query,(id, ))
  result = cursor.fetchone()
  return Boardgame(
    int(result[0]),
    int(result[1]),
    int(result[2]),
    result[3],
    result[4],
    result[5],
  )


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