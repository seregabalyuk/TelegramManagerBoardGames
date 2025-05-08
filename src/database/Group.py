import database.connect as data
import random

class Group:
  def __init__(self, id, telegram_group_id, title, password):
    self.id = id
    self.telegram_group_id = telegram_group_id
    self.title = title
    self.password = password
  
  def delete(self):
    delete1_query = """
    DELETE FROM group_member
    WHERE group_id = %s
    """

    delete2_query = """
    DELETE FROM group_users
    WHERE id = %s
    """
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(delete1_query,(self.id, ))
    cursor.execute(delete2_query,(self.id, ))
    
    connect.commit()
  
  def add(self, user):
    select_query = """
    INSERT INTO group_member (group_id, user_id) 
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
        SELECT 1 FROM group_member 
        WHERE group_id = %s AND user_id = %s
    )
    """

    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(select_query,(self.id, user.id))
    return cursor.fetchone()[0]
    


def create(telegram_group_id: int, title: str):
  select_query = """
  SELECT id, title, password
  FROM group_users 
  WHERE telegram_group_id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(telegram_group_id, ))
  result = cursor.fetchone()
  if result:
    return Group(result[0], telegram_group_id, result[1], result[2])
  else:
    password = random.randint(0, 1000_000_000)
    insert_query = """
    INSERT INTO group_users (telegram_group_id, title, password)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(insert_query,(telegram_group_id, title, password, ))
    id = cursor.fetchone()[0]
    connect.commit()
    return Group(id, telegram_group_id, title, password)


def load(group_id: int, password: int):
  select_query = """
  SELECT telegram_group_id, title
  FROM group_users 
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

