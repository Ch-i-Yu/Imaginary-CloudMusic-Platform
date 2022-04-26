# scyqy1 20318224 Qi YOU 
import logging

from flask import Flask, request, redirect, render_template, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    conn = sqlite3.connect('iMusic.db')
    #Establish a connection to the target file
    cur = conn.cursor()
    #Create a "cursor" -> "pointer?"
    conn.row_factory = sqlite3.Row
    #Maybe optional? Applied for convenience.

    cur.execute("SELECT DISTINCT Name FROM Genre ORDER BY Name ASC;")
    #Execute the sql query.
    temp_genres = cur.fetchall();
    #Grab all the tuples/rows/records. 
    genres = []
    #Create a empty list.

    for row in temp_genres:
        temp = {}
        #Create a temporary empty dictionary.
        temp['Name'] = row[0]
        #Mannualy arrange the dictionary.
        genres.append(temp)
        #Append it to the genres dictionary.

    return render_template('search.html', genres = genres)

@app.route('/search/genre', methods = ['POST'])
def search_results():
    if request.method == 'POST':
        genre = request.form['genre']
    #Grab the return value of "request"

        #print(genre) -> The value is a string

    conn = sqlite3.connect('iMusic.db')
    #Establish a connection to the target file
    conn.row_factory = sqlite3.Row
    #Maybe optional? Applied for convenience.
    cur = conn.cursor()
    #Create a "cursor" -> "pointer?"
    #SEQUENCE MATTERS!
    sql_genre_query = """
    SELECT Album.AlbumId AS AlbumId, 
            Album.Title AS AlbumTitle, 
            Artist.Name AS ArtistName, 
            SUM(Track.Milliseconds/1000) AS AlbumDuration, 
            SUM(Track.UnitPrice) AS AlbumValue
    FROM Album
        INNER JOIN Artist
        ON Album.ArtistId = Artist.ArtistId
        INNER JOIN Track
        On Album.AlbumId = Track.AlbumId
    WHERE Album.AlbumId IN (SELECT DISTINCT Track.AlbumId
                FROM Track
                WHERE Track.GenreId IN (SELECT DISTINCT Genre.GenreId
                                FROM Genre
                                WHERE Genre.Name = ?))
    GROUP BY Album.AlbumId
    ORDER BY Album.AlbumId ASC
    """
    #Introduce a block a sql-query.
    cur.execute(sql_genre_query, (genre,))
    #Execute.
    albums = cur.fetchall();
    #Grab all the tuples, translate them with a "row format"
    return render_template('results.html', genre = genre, albums = albums)

@app.route('/tracks/<string:album_id>')
def tracks(album_id):
    sql_query = """
    SELECT 
        TrackId, Name, Composer, Milliseconds AS Duration, UnitPrice as Price 
        FROM Track 
        WHERE AlbumId = ?
        ORDER BY AlbumId;
    """

    con = sqlite3.connect("iMusic.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql_query, (album_id,))
    album_tracks = cur.fetchall()
    print([a[0] for a in album_tracks])

    return render_template('track_list.html', tracks=album_tracks)

###########################################################################

@app.route('/add/')
def add():
    return render_template('add_genre.html')


@app.route('/add/genre', methods = ['POST'])
def add_genre():
    Name = request.form['genre']
    #Grab the requested data.
    if Name == '':  #"len()" not introduced.
        error = 1
        #Activiate error
        message = ["A Genre name must be provided."]
        #Provide the message
        return render_template('add_genre.html', error = error, messages = message)
    else:
        sql_Max_Id = "SELECT MAX(GenreId) FROM Genre;"
        sql_add_genre = "INSERT INTO Genre (GenreId, Name) VALUES (?, ?);"
        sql_search_exist = "SELECT COUNT(*) FROM Genre WHERE Name = ?;"
        #SET sql-query commands
        with sqlite3.connect("iMusic.db") as conn:
        #Using "with" will automatically close the connection to the
        #sqlite DB fils after the inner block completes.
            try: 
                cur = conn.cursor()
                #Create a "cursor" -> "pointer?"
                cur.execute(sql_Max_Id)
                temp1 = cur.fetchone()
                GenreId = int(temp1[0]) + 1
                #Calculate the possible GenreId for the item added
                cur.execute(sql_search_exist, (Name,))
                temp2 = cur.fetchone()
                flag = int(temp2[0])
                #Check the existence of the item
                if flag == 0:
                    cur.execute(sql_add_genre, (GenreId, Name,))
                    conn.commit()
                    #Apply the changes to DB
                    message = ["Successfully added "+Name+" to the DB."]
                    #Adjust the success-message
                    return render_template('add_genre.html', messages = message)
                else: 
                    error = 1
                    #Activiate error
                    message = ["The specific Genre is already present in the DB."]
                    return render_template('add_genre.html', error = error, messages = message)

            except BaseException:
                error = 1
                #Activiate error
                message = ["Unable to insert specified values into the database."]
                return render_template('add_genre.html', error = error, messages = message)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    