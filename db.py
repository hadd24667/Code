import mysql.connector
import pandas as pd
import numpy as np
from faker import Faker

# Kết nối và chèn dữ liệu
def insert_music_data(file_path):
    conn = mysql.connector.connect(host="localhost", user="root", password="12345678", database="music_recommender")
    cursor = conn.cursor()

    df = pd.read_csv(file_path, delimiter=',', dtype=str) 
    df = df.replace({np.nan: None, "nan": None, "": None})  
 
    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT IGNORE INTO songs (track_id, name, artist, genre, year, preview_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                int(row['track_id']),
                row['name'] or "",    
                row['artist'] or "",  
                row['genre'] or "",   
                int(row['year']),          
                row['preview_url'] or ""
            ))
            
            
        except Exception as e:
            print(f"Lỗi khi chèn dòng {row['track_id']}: {e}")

    conn.commit()
    conn.close()
    print("✅ Đã nhập xong dữ liệu songs!")

# Chạy hàm
insert_music_data("songs.csv")


def insert_random_users():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="music_recommender"
    )
    cursor = conn.cursor()

    # Tạo danh sách user ngẫu nhiên
    faker = Faker()
    user_data = [(i, faker.name()) for i in range(1, 501)]  # Tạo 500 user từ ID 1 đến 500

    # Chèn vào MySQL
    for user_id, name in user_data:
        try:
            cursor.execute('''
                INSERT IGNORE INTO users (user_id, name)
                VALUES (%s, %s)
            ''', (user_id, name))
        except Exception as e:
            print(f"Lỗi khi chèn user {user_id}: {e}")

    # Commit và đóng kết nối
    conn.commit()
    conn.close()
    print("✅ Inserted 500 random users!")

# Chạy hàm
insert_random_users()


def insert_recommendations(file_path):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="music_recommender"
    )
    cursor = conn.cursor()

    df = pd.read_csv(file_path, delimiter=',', dtype=str)

    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT IGNORE INTO recommendations (user_id, track_id, score)
                VALUES ( %s, %s, %s)
            ''', (
                int(row['user_id']),
                int(row['track_id']),
                float(row['score'])
            ))
        except Exception as e:
            print(f"Lỗi khi chèn dòng {row['id']}: {e}")

    conn.commit()
    conn.close()
    print("✅ Đã nhập xong dữ liệu recommendations!")

# Chạy hàm
insert_recommendations("recommendations.csv")

def insert_listen_history(file_path):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="music_recommender"
    )
    cursor = conn.cursor()

    df = pd.read_csv(file_path, delimiter=',', dtype=str)

    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT IGNORE INTO listen_history (user_id, track_id, playcount)
                VALUES (%s, %s, %s)
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