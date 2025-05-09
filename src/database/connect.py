import psycopg2

def connect():
  return psycopg2.connect(
    dbname="board_game_database",
    user="board_game_bot",#postgres
    password="bot",#12345678
    host="localhost",
    port="5432"
  )

