import database.connect as data

class Group:
  def __init__(self, id, telegram_group_id, title):
    self.id = id
    self.telegram_group_id = telegram_group_id
    self.title = title
  
  def delete(self):
    delete_query = """
    DELETE FROM group_users
    WHERE id = %s
    """
    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(delete_query,(self.telegram_group_id, ))
    connect.commit()



def create(telegram_group_id: int, title: str):
  select_query = """
  SELECT id, title
  FROM group_users 
  WHERE telegram_group_id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(telegram_group_id, ))
  result = cursor.fetchone()
  if result:
    return Group(result[0], telegram_group_id, result[1])
  else:
    insert_query = """
    INSERT INTO group_users (telegram_group_id, title)
    VALUES (%s, %s)
    RETURNING id;
    """

    connect = data.connect()
    cursor = connect.cursor()

    cursor.execute(insert_query,(telegram_group_id, title, ))
    id = cursor.fetchone()[0]
    connect.commit()
    return Group(id, telegram_group_id, title)


def load(telegram_group_id: int):
  select_query = """
  SELECT id, title
  FROM group_users 
  WHERE telegram_group_id = %s
  """

  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(select_query,(telegram_group_id, ))
  return Group(
    cursor.fetchone()[0], 
    telegram_group_id, 
    cursor.fetchone()[1]
  )


