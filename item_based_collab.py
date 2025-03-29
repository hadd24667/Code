import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns   
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# Dữ liệu các bài hát mới với thể loại
song_data = [
    {"song_id": 101, "song_name": "Giá Như", "artist": "Artist 1", "duration": 300, "genre": "Pop"},
    {"song_id": 102, "song_name": "Nơi Đây Có Anh", "artist": "Artist 2", "duration": 240, "genre": "Ballad"},
    {"song_id": 103, "song_name": "Thiên Lý ơi", "artist": "Artist 3", "duration": 200, "genre": "Rock"},
    {"song_id": 104, "song_name": "APT", "artist": "Artist 4", "duration": 220, "genre": "Electronic"},
    {"song_id": 105, "song_name": "Hey Daddy", "artist": "Artist 5", "duration": 260, "genre": "R&B"},
    {"song_id": 106, "song_name": "Tình Yêu Màu Nắng", "artist": "Artist 6", "duration": 230, "genre": "Pop"},
    {"song_id": 107, "song_name": "Lạc Lối", "artist": "Artist 7", "duration": 250, "genre": "Indie"},
    {"song_id": 108, "song_name": "Nhớ Em", "artist": "Artist 8", "duration": 210, "genre": "Ballad"},
    {"song_id": 109, "song_name": "Mặt Trời Của Em", "artist": "Artist 9", "duration": 230, "genre": "Pop"},
    {"song_id": 110, "song_name": "Ngày Mai Em Đi", "artist": "Artist 10", "duration": 240, "genre": "Rock"}
]

# Dữ liệu nghe nhạc của người dùng
history_data = [
    {"user_id": 1, "song_id": 101, "play_count": 5},
    {"user_id": 2, "song_id": 102, "play_count": 3},
    {"user_id": 1, "song_id": 103, "play_count": 4},
    {"user_id": 3, "song_id": 104, "play_count": 7},
    {"user_id": 4, "song_id": 101, "play_count": 6},
    {"user_id": 5, "song_id": 105, "play_count": 8},
    {"user_id": 2, "song_id": 106, "play_count": 5},
    {"user_id": 6, "song_id": 107, "play_count": 2},
    {"user_id": 7, "song_id": 108, "play_count": 4},
    {"user_id": 8, "song_id": 109, "play_count": 3},
    {"user_id": 9, "song_id": 110, "play_count": 6},
    {"user_id": 3, "song_id": 105, "play_count": 4},
    {"user_id": 5, "song_id": 106, "play_count": 3},
    {"user_id": 7, "song_id": 107, "play_count": 5},
    {"user_id": 8, "song_id": 101, "play_count": 4},
    {"user_id": 9, "song_id": 110, "play_count": 7},
    {"user_id": 10, "song_id": 102, "play_count": 5},
    {"user_id": 10, "song_id": 104, "play_count": 6}
]

# Chuyển đổi thành DataFrame cho các bài hát và lịch sử nghe nhạc
song_df = pd.DataFrame(song_data)
history_df = pd.DataFrame(history_data)

# Tạo ma trận user-song (lượt phát)
rating_matrix = history_df.pivot_table(index='user_id', columns='song_id', values='play_count', fill_value=0)

# One-hot encoding cho thể loại
encoder = OneHotEncoder(sparse_output=False)
genre_encoded = encoder.fit_transform(song_df[['genre']])
genre_df = pd.DataFrame(genre_encoded, columns=encoder.get_feature_names_out(['genre']), index=song_df['song_id'])

# Kết hợp ma trận rating với dữ liệu thể loại
rating_matrix_with_genre = rating_matrix.T.join(genre_df, how='left')

# Tính cosine similarity giữa các bài hát
song_similarity = cosine_similarity(rating_matrix_with_genre.fillna(0))

# Chuyển đổi kết quả thành DataFrame để dễ dàng xem
song_similarity_df = pd.DataFrame(song_similarity, index=song_df['song_id'], columns=song_df['song_id'])

# In kết quả
print(song_similarity_df)

# Vẽ heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(song_similarity_df, annot=True, cmap="YlGnBu", fmt=".1f", cbar_kws={'label': 'Similarity'})
plt.title("Song-Song Similarity Heatmap (Including Genre and Play Count)", fontsize=16)
plt.xlabel("Song ID", fontsize=12)
plt.ylabel("Song ID", fontsize=12)
plt.show()