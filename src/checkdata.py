import psycopg2

connect = psycopg2.connect(
dbname="board_game_database",
user="board_game_bot",
password="bot",
host="localhost",
port="5432"
)

cursor = connect.cursor()