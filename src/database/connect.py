import psycopg2

def connect():
  return psycopg2.connect(
    dbname="board_game_database",
    user="postgres",
    password="12345678",
    host="localhost",
    port="5432"
  )

