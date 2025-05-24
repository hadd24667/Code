import pyodbc
import pandas as pd
import numpy as np
from faker import Faker

# Hàm kết nối SQL Server
def get_connection():
    conn_str = (
        "DRIVER={SQL Server};"
        "SERVER=localhost\\MSSQLSERVER01;"
        "DATABASE=music_recommender;"
        "UID=sa;"
        "PWD=12345678;" 
    )
    return pyodbc.connect(conn_str)

# Hàm chèn dữ liệu songs
def insert_music_data(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_csv(file_path, delimiter=',', dtype=str)
    df = df.replace({np.nan: None, "nan": None, "": None})

    for _, row in df.iterrows():
        try:
            # Kiểm tra xem track_id đã tồn tại chưa
            cursor.execute("SELECT COUNT(*) FROM songs WHERE track_id = ?", (int(row['track_id']),))
            if cursor.fetchone()[0] == 0:  # Nếu chưa tồn tại
                cursor.execute('''
                    INSERT INTO songs (track_id, name, artist, genre, year, preview_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['track_id']),
                    row['name'] or "",
                    row['artist'] or "",
                    row['genre'] or "",
                    int(row['year']) if row['year'] is not None else 0,
                    row['preview_url'] or ""
                ))
        except Exception as e:
            print(f"Lỗi khi chèn dòng {row['track_id']}: {e}")

    conn.commit()
    conn.close()
    print("✅ Đã nhập xong dữ liệu songs!")

# Chạy hàm
insert_music_data("songs.csv")

# Hàm chèn dữ liệu users
def insert_random_users():
    conn = get_connection()
    cursor = conn.cursor()

    # Tạo danh sách user ngẫu nhiên
    faker = Faker()
    user_data = [(i, faker.name()) for i in range(1, 501)]  # Tạo 500 user

    for user_id, name in user_data:
        try:
            # Kiểm tra xem user_id đã tồn tại chưa
            cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone()[0] == 0:  # Nếu chưa tồn tại
                cursor.execute('''
                    INSERT INTO users (user_id, name)
                    VALUES (?, ?)
                ''', (user_id, name))
        except Exception as e:
            print(f"Lỗi khi chèn user {user_id}: {e}")

    conn.commit()
    conn.close()
    print("✅ Inserted 500 random users!")

# Chạy hàm
insert_random_users()

# Hàm chèn dữ liệu recommendations
def insert_recommendations(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_csv(file_path, delimiter=',', dtype=str)

    for _, row in df.iterrows():
        try:
            # Kiểm tra xem cặp user_id, track_id đã tồn tại chưa
            cursor.execute("SELECT COUNT(*) FROM recommendations WHERE user_id = ? AND track_id = ?",
                          (int(row['user_id']), int(row['track_id'])))
            if cursor.fetchone()[0] == 0:  # Nếu chưa tồn tại
                cursor.execute('''
                    INSERT INTO recommendations (user_id, track_id, score)
                    VALUES (?, ?, ?)
                ''', (
                    int(row['user_id']),
                    int(row['track_id']),
                    float(row['score'])
                ))
        except Exception as e:
            print(f"Lỗi khi chèn dòng user_id={row['user_id']}, track_id={row['track_id']}: {e}")

    conn.commit()
    conn.close()
    print("✅ Đã nhập xong dữ liệu recommendations!")

# Chạy hàm
insert_recommendations("recommendations.csv")

# Hàm chèn dữ liệu listen_history
def insert_listen_history(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_csv(file_path, delimiter=',', dtype=str)

    for _, row in df.iterrows():
        try:
            # Kiểm tra xem cặp user_id, track_id đã tồn tại chưa
            cursor.execute("SELECT COUNT(*) FROM listen_history WHERE user_id = ? AND track_id = ?",
                          (int(row['user_id']), int(row['track_id'])))
            if cursor.fetchone()[0] == 0:  # Nếu chưa tồn tại
                cursor.execute('''
                    INSERT INTO listen_history (user_id, track_id, playcount)
                    VALUES (?, ?, ?)
                ''', (
                    int(row['user_id']),
                    int(row['track_id']),
                    int(row['playcount'])
                ))
        except Exception as e:
            print(f"Lỗi khi chèn dòng user_id={row['user_id']}, track_id={row['track_id']}: {e}")

    conn.commit()
    conn.close()
    print("✅ Đã nhập xong dữ liệu listen_history!")

# Chạy hàm
insert_listen_history("listen_history.csv")