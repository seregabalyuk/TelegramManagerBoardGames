import database.connect as data

class User:
  def __init__(self, id, telegram_id, name):
    self.id = id
    self.telegram_id = telegram_id
    self.name = name



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
  return User(id, telegram_id, name)


def load(telegram_id: int):
  select_query = """
  SELECT id, name
  FROM users 
  WHERE telegram_id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(telegram_id, ))
  return User(
    cursor.fetchone()[0], 
    telegram_id, 
    cursor.fetchone()[1]
  )


def get(telegram_id: int, name: str):
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
    return User(result[0], telegram_id, result[1])
  else:
    return register(telegram_id, name)


