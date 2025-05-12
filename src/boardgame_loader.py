import database.connect as data

from shops import hobbygames


for i in range(1, 40):
  games = hobbygames.load(i, i)
  insert_query = """
  INSERT INTO types_boardgames (
      name, 
      min_players, 
      max_players, 
      min_playing_time, 
      max_playing_time, 
      age, 
      image_url
  ) VALUES (
      %s,
      %s,
      %s,
      %s,
      %s,
      %s,
      %s
  )
  """
 

  for game in games:
    try:
      connect = data.connect()
      cursor = connect.cursor()
      cursor.execute(
        insert_query,
        (
          game[0], 
          game[1][0],
          game[1][1],
          game[2][0],
          game[2][1],
          game[3][0],
          game[5],
        )
      )
      connect.commit()
    except Exception as exs:
      print(exs)
      print(f"Not insert; {game[0]}")
      print(game)
  print("load to database")
  
