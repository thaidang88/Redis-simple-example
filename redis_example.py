import redis
import json
import time

# 1. Khởi tạo kết nối tới Redis Server (Mặc định chạy ở port 6379)
# decode_responses=True giúp tự động chuyển đổi định dạng byte nhận được từ Redis sang chuỗi (string)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Hàm giả lập việc lấy dữ liệu từ Database thật (MySQL/PostgreSQL) rất chậm
def fetch_user_from_database(user_id):
    print(f"⏳ [Database] Đang quét đĩa cứng tìm User {user_id}...")
    time.sleep(2) # Giả lập độ trễ truy vấn mất 2 giây
    return {
        "id": user_id,
        "name": "Alex Nguyen",
        "role": "Software Engineer",
        "company": "xxxxx Company"
    }

# Hàm lấy thông tin User có áp dụng Redis Cache
def get_user_profile(user_id):
    cache_key = f"user:profile:{user_id}"
    
    # 2. Thử lấy dữ liệu từ Redis Cache trước
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        print("🚀 [Redis] CACHE HIT! Lấy dữ liệu từ RAM siêu tốc (~1ms)")
        # Chuyển chuỗi JSON từ cache ngược lại thành Dict của Python
        return json.loads(cached_data)
    
    # 3. CACHE MISS: Nếu cache chưa có, bắt buộc phải vào Database lấy
    print("⚠️ [Redis] CACHE MISS! Dữ liệu không tồn tại trong cache.")
    user_data = fetch_user_from_database(user_id)
    
    # 4. Lưu bản sao dữ liệu vào Redis Cache
    # Sử dụng setex để vừa set dữ liệu vừa cấu hình TTL (Time-To-Live). Ở đây đặt 60 giây.
    # Sau 60 giây, dữ liệu này sẽ tự động xóa khỏi RAM để tiết kiệm dung lượng.
    redis_client.setex(
        name=cache_key,
        time=60,
        value=json.dumps(user_data) # Chuyển Dict thành chuỗi JSON để lưu trữ
    )
    print(f"💾 [Redis] Đã lưu bản sao của User {user_id} vào cache (Hết hạn sau 60s).")
    
    return user_data

# --- CHẠY THỬ NGHIỆM ---
if __name__ == "__main__":
    USER_ID = 99
    
    print("--- LUỒNG CHẠY LẦN 1 (Cache trống) ---")
    start_time = time.time()
    user1 = get_user_profile(USER_ID)
    print(f"Kết quả Lần 1: {user1['name']} - Xử lý mất: {time.time() - start_time:.2f} giây\n")
    
    print("--- LUỒNG CHẠY LẦN 2 (Đã có Cache) ---")
    start_time = time.time()
    user2 = get_user_profile(USER_ID)
    print(f"Kết quả Lần 2: {user2['name']} - Xử lý mất: {time.time() - start_time:.4f} giây\n")
