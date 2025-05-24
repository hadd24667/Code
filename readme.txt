cài thư viện python
   pip install fastapi mysql-connector-python uvicorn faker pandas numpy
   pip install fastapi[all]
tạo database 
   dùng schema trong dbSchema.txt
Import database
    vô db.py nếu cần thì sửa password ở các hàm ( mặc định đang là null)
Run api server
    vô main.py run " uvicorn main:app --reload  " ở terminal
    Các api gồm
    GET /user/{user_id}   : Get thông tin user , chỉ có tên
        ví dụ: localhost:8000/user/1
    GET /user/{user_id}/history
          
    GET /user/{user_id}/recommendations

   
//hieu update

Hiện tại đang dùng sql nên đây là list cần sửa để dùng sang mysql
merge: (nếu dùng mySQL)
    + file db.py đừng merge của t vô (tại t sửa để dùng sql -> lấy file cũ)
    + main.py : lấy get_top_played_songs, get_db_connection của file cũ, nhớ import mysql.connector 
    + dashboard merge bình thường
