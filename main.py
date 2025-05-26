from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://127.0.0.1:5500/", "http://localhost:5500/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hàm kết nối SQL Server
def get_db_connection():
    conn_str = (
        "DRIVER={SQL Server};"
        "SERVER=localhost\\MSSQLSERVER01;"
        "DATABASE=music_recommender;"
        "UID=sa;"
        "PWD=12345678;"
    )
    return pyodbc.connect(conn_str)

# 1️⃣ API lấy thông tin người dùng
@app.get("/user/{user_id}")
def get_user_info(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, name FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Chuyển đổi kết quả thành dictionary
    return {"user_id": user[0], "name": user[1]}

# 2️⃣ API lấy danh sách gợi ý
@app.get("/user/{user_id}/recommendations")
def get_recommendations(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP 10
            r.track_id, s.name AS song_name, s.artist, s.genre, s.year, s.preview_url, r.score
        FROM recommendations r
        JOIN songs s ON r.track_id = s.track_id
        WHERE r.user_id = ?
        ORDER BY r.score DESC
    """, (user_id,))
    recommendations = cursor.fetchall()

    cursor.close()
    conn.close()

    # Chuyển đổi kết quả thành danh sách dictionary
    recommendations_list = [
        {
            "track_id": row[0],
            "song_name": row[1],
            "artist": row[2],
            "genre": row[3],
            "year": row[4],
            "preview_url": row[5],
            "score": row[6]
        } for row in recommendations
    ]

    return {"user_id": user_id, "recommendations": recommendations_list}

# 3️⃣ API lấy lịch sử nghe nhạc
@app.get("/user/{user_id}/history")
def get_listening_history(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            lh.track_id, s.name AS song_name, s.artist, s.genre, s.year, s.preview_url, lh.playcount
        FROM listen_history lh
        JOIN songs s ON lh.track_id = s.track_id
        WHERE lh.user_id = ?
        ORDER BY lh.playcount DESC
    """, (user_id,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()

    # Chuyển đổi kết quả thành danh sách dictionary
    history_list = [
        {
            "track_id": row[0],
            "song_name": row[1],
            "artist": row[2],
            "genre": row[3],
            "year": row[4],
            "preview_url": row[5],
            "playcount": row[6]
        } for row in history
    ]

    return {"user_id": user_id, "listening_history": history_list}

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
    cursor = conn.cursor()

    query = f"""
        SELECT TOP {limit}
            s.track_id,
            s.name AS title,
            s.artist,
            s.genre,
            s.year,
            s.preview_url AS url,
            SUM(lh.playcount) AS total_playcount
        FROM listen_history lh
        JOIN songs s ON lh.track_id = s.track_id
        GROUP BY s.track_id, s.name, s.artist, s.genre, s.year, s.preview_url
        ORDER BY total_playcount DESC
    """
    cursor.execute(query)
    top_songs = cursor.fetchall()

    cursor.close()
    conn.close()

    top_songs_list = [
        {
            "track_id": row[0],
            "title": row[1],
            "artist": row[2],
            "genre": row[3],
            "year": row[4],
            "url": row[5],
            "total_playcount": row[6]
        } for row in top_songs
    ]

    return {"top_played_songs": top_songs_list}