import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Dữ liệu từ SQL
history_data = [
    {"user_id": 1, "song_id": 101, "play_count": 5, "total_duration": 300},
    {"user_id": 2, "song_id": 101, "play_count": 2, "total_duration": 120},
    {"user_id": 1, "song_id": 102, "play_count": 3, "total_duration": 180},
    {"user_id": 3, "song_id": 103, "play_count": 7, "total_duration": 420},
    {"user_id": 4, "song_id": 101, "play_count": 4, "total_duration": 240},
    {"user_id": 5, "song_id": 104, "play_count": 6, "total_duration": 360},
    {"user_id": 2, "song_id": 103, "play_count": 8, "total_duration": 480},
    {"user_id": 6, "song_id": 105, "play_count": 3, "total_duration": 180},
    {"user_id": 7, "song_id": 102, "play_count": 5, "total_duration": 300},
    {"user_id": 8, "song_id": 104, "play_count": 2, "total_duration": 120},
    {"user_id": 9, "song_id": 105, "play_count": 9, "total_duration": 540},
    {"user_id": 10, "song_id": 101, "play_count": 1, "total_duration": 60},
    {"user_id": 3, "song_id": 102, "play_count": 4, "total_duration": 240},
    {"user_id": 4, "song_id": 105, "play_count": 7, "total_duration": 420},
    {"user_id": 5, "song_id": 103, "play_count": 5, "total_duration": 300},
    {"user_id": 6, "song_id": 102, "play_count": 3, "total_duration": 180},
    {"user_id": 7, "song_id": 104, "play_count": 6, "total_duration": 360},
    {"user_id": 8, "song_id": 101, "play_count": 8, "total_duration": 480},
    {"user_id": 9, "song_id": 103, "play_count": 2, "total_duration": 120},
    {"user_id": 10, "song_id": 102, "play_count": 4, "total_duration": 240},
    {"user_id": 1, "song_id": 104, "play_count": 5, "total_duration": 300},
    {"user_id": 2, "song_id": 105, "play_count": 6, "total_duration": 360}
]

# Chuyển đổi thành DataFrame
history_df = pd.DataFrame(history_data)

# Tạo ma trận user-song
rating_matrix = history_df.pivot_table(
    index='user_id', 
    columns='song_id', 
    values='play_count',
    fill_value=0
)

print("User-Song Rating Matrix: ")
print(rating_matrix)

# Vẽ heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(rating_matrix, annot=True, cmap="YlGnBu", fmt=".1f", cbar_kws={'label': 'Play Count'})

# Gắn nhãn
plt.title("User-Song Play Count Heatmap", fontsize=16)
plt.xlabel("Song ID", fontsize=12)
plt.ylabel("User ID", fontsize=12)
plt.show()

# Tính toán độ tương tự giữa các user (transpose matrix first)
user_similarity = rating_matrix.T.corr()
print("User Similarity Matrix: ")
print(user_similarity)

# Vẽ heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(user_similarity, annot=True, cmap="YlGnBu", fmt=".2f", 
            cbar_kws={'label': 'Similarity'},
            xticklabels=[f"User {id}" for id in user_similarity.columns],
            yticklabels=[f"User {id}" for id in user_similarity.index])

# Gắn nhãn
plt.title("User Similarity Heatmap", fontsize=16)
plt.xlabel("User ID", fontsize=12)
plt.ylabel("User ID", fontsize=12)
plt.tight_layout()
plt.show()
