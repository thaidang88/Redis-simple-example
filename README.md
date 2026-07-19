# Redis-simple-example

Chuẩn bị môi trường:
Bash
pip install redis

Kết quả trên Terminal sẽ hiển thị dạng:
Plaintext
--- LUỒNG CHẠY LẦN 1 (Cache trống) ---
⚠️ [Redis] CACHE MISS! Dữ liệu không tồn tại trong cache.
⏳ [Database] Đang quét đĩa cứng tìm User 99...
💾 [Redis] Đã lưu bản sao của User 99 vào cache (Hết hạn sau 60s).
Kết quả Lần 1: Alex Nguyen - Xử lý mất: 2.01 giây

--- LUỒNG CHẠY LẦN 2 (Đã có Cache) ---
🚀 [Redis] CACHE HIT! Lấy dữ liệu từ RAM siêu tốc (~1ms)
Kết quả Lần 2: Alex Nguyen - Xử lý mất: 0.0008 giây
