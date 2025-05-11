import database.connect as data

class User:
  def __init__(self, id:int, telegram_id:int, name):
    self.id = id
    self.telegram_id = telegram_id
    self.name = name

  def add_boardgame(self, type_boardgame_id: int, is_bought: bool):
    try:
      insert_query = """
      INSERT INTO boardgames (
        owner_user_id, 
        type_boardgame_id,
        is_bought
      )
      VALUES (%s, %s, %s);
      """
      connect = data.connect()
      cursor = connect.cursor()

      cursor.execute(insert_query,(self.id, type_boardgame_id, is_bought, ))
      connect.commit()
      return True
    except:
      return False

  def check_game(self, game_id: int) :
    connect = data.connect()
    cursor = connect.cursor()
    cursor.execute("""
      SELECT took_user_id, is_bought 
      FROM boardgames 
      WHERE owner_user_id = %s 
      AND type_boardgame_id = %s""", 
      (self.id, game_id)
    )
    return cursor.fetchone()

  def get_friends(self, with_game_id=None ):#вуаu Na
    connect = data.connect()
    cursor = connect.cursor()
    if with_game_id is None :
      cursor.execute("SELECT users.name, groups.name, users.telegram_id FROM groups_members JOIN users ON users.id = user_id JOIN groups ON groups.id = group_id WHERE group_id IN (SELECT group_id FROM groups_members WHERE user_id = %s)", (int(self.id), ))

    else :
      cursor.execute("WITH with_game AS (SELECT owner_user_id, took_user_id, is_bought FROM boardgames WHERE type_boardgame_id = %s) SELECT users.id, took_user_id, is_bought, users.name, groups.name, users.telegram_id FROM groups_members JOIN users ON users.id = user_id JOIN groups ON groups.id = group_id JOIN with_game ON with_game.owner_user_id = user_id WHERE group_id IN (SELECT group_id FROM groups_members WHERE user_id = %s)", (int(with_game_id), int(self.id)))
    return cursor.fetchall()

  def get_leased_games(self):
    connect = data.connect()
    cursor = connect.cursor()
    cursor.execute("SELECT users.name, users.telegram_id, types_boardgames.name, boardgames.id FROM boardgames JOIN users ON users.id = owner_user_id JOIN types_boardgames ON types_boardgames.id = type_boardgame_id WHERE took_user_id = %s;", (self.id, ))
    return cursor.fetchall()

def register(telegram_id: int, name: str):
  insert_query = """
  INSERT INTO users (telegram_id, name)
  VALUES (%s, %s)
  RETURNING id;
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(insert_query,(telegram_id, name, ))
  id = cursor.fetchone()[0]
  connect.commit()
  return User(int(id), telegram_id, name)


def load(telegram_id: int):
  select_query = """
  SELECT id, name
  FROM users 
  WHERE telegram_id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(telegram_id, ))
  res = cursor.fetchone()

  return User(
    int(res[0]),
    telegram_id, 
    res[1]
  )


def get(telegram_id: int, name: str, registreted=False):
  select_query = """
  SELECT id, name
  FROM users 
  WHERE telegram_id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(telegram_id, ))
  result = cursor.fetchone()
  if result:
    registreted = False
    return User(int(result[0]), telegram_id, result[1])
  else:
    registreted = True
    return register(telegram_id, name)

