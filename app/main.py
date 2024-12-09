from fastapi import FastAPI
import mysql.connector
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection details
DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "unb6ny"

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)

@app.get('/genres')
def get_genres():
    db = get_db_connection()
    cur = db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        cur.close()
        db.close()
        return json_data
    except mysql.connector.Error as e:
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}

@app.get("/songs")
def get_songs():
    # Connect to MySQL database
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur = db.cursor()

    # SQL query to join the songs and genres tables
    query = """
    SELECT 
        songs.title, 
        songs.album, 
        songs.artist, 
        songs.year, 
        songs.file, 
        songs.image, 
        genres.genre
    FROM songs 
    JOIN genres ON songs.genre = genres.genreid 
    ORDER BY songs.songid;
    """
    try:
        cur.execute(query)
        
        # Fetch headers from the cursor description (column names)
        headers = [x[0] for x in cur.description]
        
        # Fetch all results
        results = cur.fetchall()
        
        # Prepare a list of dictionaries to return as JSON
        json_data = []
        for result in results:
            json_data.append({
                "title": result[0],
                "album": result[1],
                "artist": result[2],
                "year": result[3],
                "file": f"https://unb6ny-dp1-spotify.s3.amazonaws.com/Songs/{result[4]}",  # S3 MP3 file URL
                "image": f"https://unb6ny-dp1-spotify.s3.amazonaws.com/Songs/{result[5]}",  # S3 image file URL
                "genre": result[6]  # Genre from the genres table
            })

        # Close database connection
        cur.close()
        db.close()

        # Return the data as JSON
        return json_data

    except Error as e:
        # In case of error, close the connection and return the error
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}
