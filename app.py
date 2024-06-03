from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL configuration
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yes",
        database="music_recommender"
    )
    if db.is_connected():
        print("Successfully connected to the database")
except Error as e:
    print(f"Error connecting to MySQL Platform: {e}")

# Get user recommendations
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT title, artist 
            FROM songs 
            WHERE genre IN (
                SELECT favorite_genres FROM users WHERE user_id = %s
            ) OR artist IN (
                SELECT favorite_artists FROM users WHERE user_id = %s
            ) OR mood IN (
                SELECT preferred_moods FROM users WHERE user_id = %s
            )
        """, (user_id, user_id, user_id))
        
        recommendations = cursor.fetchall()
        return jsonify(recommendations)
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Add user profile
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    try:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO users (name, favorite_genres, favorite_artists, preferred_moods) 
            VALUES (%s, %s, %s, %s)
        """, (data['name'], ','.join(data['favorite_genres']), ','.join(data['favorite_artists']), ','.join(data['preferred_moods'])))
        db.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

