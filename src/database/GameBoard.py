import database.connect as data


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