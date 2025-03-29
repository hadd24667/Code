from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI()

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="music_recommender"
    )

# 1️⃣ API lấy thông tin người dùng
@app.get("/user/{user_id}")
def get_user_info(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id, name FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user


# 2️⃣ API lấy danh sách gợi ý
@app.get("/user/{user_id}/recommendations")
def get_recommendations(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.track_id, s.name AS song_name, s.artist, s.genre, s.year, s.preview_url, r.score
        FROM recommendations r
        JOIN songs s ON r.track_id = s.track_id
        WHERE r.user_id = %s
        ORDER BY r.score DESC
        LIMIT 10
    """, (user_id,))
    recommendations = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"user_id": user_id, "recommendations": recommendations}


# 3️⃣ API lấy lịch sử nghe nhạc
@app.get("/user/{user_id}/history")
def get_listening_history(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT lh.track_id, s.name AS song_name, s.artist, s.genre, s.year, s.preview_url, lh.playcount
        FROM listen_history lh
        JOIN songs s ON lh.track_id = s.track_id
        WHERE lh.user_id = %s
        ORDER BY lh.playcount DESC
    """, (user_id,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"user_id": user_id, "listening_history": history}

# 4️⃣ API: Thống kê tổng quan
@app.get("/dashboard/summary")
def get_dashboard_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM songs")
    total_songs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM recommendations")
    total_recommendations = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(playcount) FROM listen_history")
    total_plays = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return {
        "users": total_users,
        "songs": total_songs,
        "recommendations": total_recommendations,
        "total_plays": total_plays
    }


# 5️⃣ API: Top bài hát được nghe nhiều nhất
@app.get("/dashboard/top-played-songs")
def get_top_played_songs(limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            s.track_id,
            s.name AS title,
            s.artist,
            s.genre,
            s.year,
            s.preview_url AS url,
            SUM(lh.playcount) AS total_playcount
        FROM listen_history lh
        JOIN songs s ON lh.track_id = s.track_id
        GROUP BY lh.track_id
        ORDER BY total_playcount DESC
        LIMIT %s
    """, (limit,))
    
    top_songs = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"top_played_songs": top_songs}

