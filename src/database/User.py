import database.connect as data

class Data:
  pass

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
    return cursor.fetchall()

  def get_friends(self, with_game_id:int|None=None, is_bought:bool=True):#вуаu Na
    connect = data.connect()
    cursor = connect.cursor()
    if with_game_id is None :
      cursor.execute("""
      SELECT DISTINCT u.*, g.id as group_id, g.name as group_name
      FROM users user_a
      JOIN groups_members gm_a ON user_a.id = gm_a.user_id
      JOIN groups g ON gm_a.group_id = g.id
      JOIN groups_members gm_other ON g.id = gm_other.group_id
      JOIN users u ON gm_other.user_id = u.id
      WHERE user_a.id = %s
        AND u.id != %s
      """, (int(self.id), int(self.id)))
    else :
      cursor.execute("""
      SELECT DISTINCT other_users.*, g.id as group_id, g.name as group_name, bg.id as game_id, bg.took_user_id as took_id
      FROM users user_a
      JOIN groups_members gm_a ON user_a.id = gm_a.user_id
      JOIN groups g ON gm_a.group_id = g.id
      JOIN groups_members gm_other ON g.id = gm_other.group_id
      JOIN users other_users ON gm_other.user_id = other_users.id
      JOIN boardgames bg ON other_users.id = bg.owner_user_id
      WHERE user_a.id = %s
        AND bg.type_boardgame_id = %s
        AND other_users.id != %s
        AND bg.is_bought = %s
      """, (self.id, with_game_id, self.id, is_bought))
    out = []
    for ans in cursor.fetchall():
      obj = Data()
      obj.user = User(int(ans[0]), int(ans[1]), ans[2])
      obj.group = Data()
      obj.group.id = int(ans[3])
      obj.group.name = ans[4]

      if not with_game_id is None:
        obj.game = Data()
        obj.game.id = int(ans[5])
        obj.game.took = ans[6]
        obj.game.name = None
        
      
      out.append(obj)
    return out

  def give_game(self, game_id:int, user_other):
    update_query = """
    WITH updated AS (
      UPDATE boardgames
      SET took_user_id = %s
      WHERE id = %s AND took_user_id IS NULL
      RETURNING 1
    )
    SELECT EXISTS (SELECT 1 FROM updated) AS success;
    """
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(update_query,(user_other.id, game_id, ))
    can = cursor.fetchone()[0]
    connect.commit()
    return can

  def get_leased_games(self):
    connect = data.connect()
    cursor = connect.cursor()
    cursor.execute("""
    SELECT users.name, users.telegram_id, types_boardgames.name, boardgames.id 
    FROM boardgames 
    JOIN users 
    ON users.id = owner_user_id 
    JOIN types_boardgames 
    ON types_boardgames.id = type_boardgame_id 
    WHERE took_user_id = %s;""", 
    (self.id, ))
    return cursor.fetchall()

  def get_games(self, is_bought = True):
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute("""
    SELECT types_boardgames.name, took_user_id, type_boardgame_id, boardgames.id
    FROM boardgames JOIN types_boardgames 
    ON types_boardgames.id = type_boardgame_id 
    WHERE owner_user_id = %s AND is_bought = %s
    """, (self.id, is_bought))
    return cursor.fetchall()

  def get_groups(self):
    connect = data.connect()
    cursor = connect.cursor()
    cursor.execute("SELECT groups.telegram_id, groups.name FROM groups_members JOIN groups ON groups.id = group_id JOIN users ON users.id = user_id WHERE users.telegram_id = %s;", (self.telegram_id, ))

    return cursor.fetchall()


  def __str__(self):
    return str(self.id) + " " + str(self.telegram_id) + " " + self.name
  
  def __repr__(self):
    return self.id.__repr__() + " " + self.telegram_id.__repr__() + " " + self.name

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


def get(telegram_id: int, name: str, registreted=True):
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
    registreted = [False]
    return User(int(result[0]), telegram_id, result[1])
  else:
    registreted = [True]
    return register(telegram_id, name)


def load_by_id(id:int):
  select_query = """
  SELECT telegram_id, name
  FROM users 
  WHERE id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(id, ))
  res = cursor.fetchone()
  if res is None:
    return None
  return User(
    id,
    int(res[0]), 
    res[1]
  )


def load_by_name(name:str):
  select_query = """
  SELECT id, telegram_id
  FROM users 
  WHERE name = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(name, ))
  res = cursor.fetchone()
  if res is None:
    return None
  return User(
    int(res[0]),
    int(res[1]), 
    name
  )