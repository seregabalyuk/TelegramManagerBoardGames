import database.connect as data
import random

from  database import User


class Group:
  def __init__(self, id, telegram_id, name, password):
    self.id = id
    self.telegram_id = telegram_id
    self.name = name
    self.password = password
  
  def delete(self):
    delete1_query = """
    DELETE FROM groups_members
    WHERE group_id = %s
    """

    delete2_query = """
    DELETE FROM groups
    WHERE id = %s
    """
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(delete1_query,(self.id, ))
    cursor.execute(delete2_query,(self.id, ))
    
    connect.commit()
  
  def add(self, user):
    select_query = """
    INSERT INTO groups_members (group_id, user_id) 
    VALUES (%s, %s) 
    ON CONFLICT (group_id, user_id) DO NOTHING
    """
    connect = data.connect()
    cursor = connect.cursor()
    cursor.execute(select_query,(self.id, user.id, ))
    connect.commit()

  def contain(self, user):
    select_query = """
    SELECT EXISTS (
        SELECT 1 FROM groups_members 
        WHERE group_id = %s AND user_id = %s
    )
    """

    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(select_query,(self.id, user.id))
    return cursor.fetchone()[0]
  
  def all_users(self):
    select_query = """
    SELECT id, telegram_id, name
    FROM groups_members 
    WHERE group_id = %s
    """
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(select_query,(self.id,))
    answer = []
    for string in cursor.fetchall():
      answer.append(int(string[0]), int(string[1]), string[2])
    return answer

  def all_gameboards(self):
    select_query = """
    SELECT bg.id, tbg.name, u.id, u.telegram_id, u.name
    FROM boardgames bg
    JOIN types_boardgames tbg ON bg.type_boardgame_id = tbg.id
    JOIN users u ON bg.owner_user_id = u.id
    JOIN groups_members gm ON u.id = gm.user_id
    JOIN groups g ON gm.group_id = g.id
    WHERE g.id = %s AND bg.is_bought = TRUE AND bg.took_user_id IS NULL;
    """
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(select_query,(self.id,))
    out = cursor.fetchall()
    games = []
    for id, name, u_id, u_tg, u_name in out:
      games.append((int(id),name, User.User(int(u_id), int(u_tg), u_name)))
    return games
      



def create(telegram_id: int, name: str):
  select_query = """
  SELECT id, name, password
  FROM groups 
  WHERE telegram_id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(telegram_id, ))
  result = cursor.fetchone()
  if result:
    return Group(result[0], telegram_id, result[1], result[2])
  else:
    password = random.randint(0, 1000_000_000)
    insert_query = """
    INSERT INTO groups (telegram_id, name, password)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(insert_query,(telegram_id, name, password, ))
    id = cursor.fetchone()[0]
    connect.commit()
    return Group(id, telegram_id, name, password)


def load(group_id: int, password: int):
  select_query = """
  SELECT telegram_id, name
  FROM groups 
  WHERE id = %s AND password = %s
  """
  
  connect = data.connect()
  cursor = connect.cursor()
  cursor.execute(select_query,(group_id, password, ))
  result = cursor.fetchone()
  return Group(
    group_id, 
    result[0],
    result[1],
    password
  )


def load_without_password(telegram_id: int):
  select_query = """
  SELECT id, name, password
  FROM groups 
  WHERE telegram_id = %s
  """
  
  connect = data.connect()
  cursor = connect.cursor()
  cursor.execute(select_query,(telegram_id, ))
  result = cursor.fetchone()
  return Group(
    int(result[0]),
    telegram_id,
    result[1],
    int(result[2])
  )