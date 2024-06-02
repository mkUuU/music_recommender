from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='music_recommender',
            user='root',
            password='yes'
        )
    except Error as e:
        print(f"Error: {e}")
    return connection

# Route to get all songs
@app.route('/songs', methods=['GET'])
def get_songs():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(songs)

# Route to get a specific song by id
@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM songs WHERE song_id = %s", (song_id,))
    song = cursor.fetchone()
    cursor.close()
    connection.close()
    if song:
        return jsonify(song)
    else:
        return jsonify({"error": "Song not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

