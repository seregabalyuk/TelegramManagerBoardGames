import database.connect as data


def find(name: str):
  find_query = """
  SELECT id, name FROM games 
  WHERE name ILIKE %s
  """ 
  search_pattern = f"%{name}%"


  connect = data.connect()
  cursor = connect.cursor()

  cursor.execute(find_query,(search_pattern, ))