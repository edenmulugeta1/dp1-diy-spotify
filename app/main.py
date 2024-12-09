from fastapi import FastAPI
import mysql.connector

app = FastAPI()

db = mysql.connector.connect(
    DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
    DBUSER = "admin"
    DBPASS = os.getenv('DBPASS')
    DB = "xxxxx"
)
cur = db.cursor()

@app.get("/songs")
async def get_songs():
    cur.execute("SELECT * FROM songs")
    return cur.fetchall()

@app.get("/genres")
async def get_genres():
    cur.execute("SELECT * FROM genres")
    return cur.fetchall()
