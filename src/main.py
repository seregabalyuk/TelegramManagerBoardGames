import psycopg2

connect = psycopg2.connect(
dbname="board_game_database",
user="postgres",
password="12345678",
host="localhost",
port="5432"
)

cursor = connect.cursor()
cursor.execute("INSERT INTO users (telegram_id, username) VALUES (%s, %s);", ("chl*n", "h*i"))