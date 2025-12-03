import yt_dlp
import json
import time

def get_quick_metadata(video_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        
        # --- CẤU HÌNH TĂNG TỐC ---
        'extract_flat': True,  # QUAN TRỌNG NHẤT: Không phân tích luồng video (stream formats)
        'force_generic_extractor': False, # Dùng extractor chuyên biệt của Youtube để nhanh hơn
        
        # Bỏ qua các bước kiểm tra không cần thiết
        'check_formats': False, 
        'write_pages': False, 
        'no_warnings': True,
        'ignoreerrors': True,
    }

    start_time = time.time() # Đo thời gian để bạn thấy sự khác biệt

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # extract_info lúc này sẽ trả về dữ liệu thô cực nhanh
            info = ydl.extract_info(video_url, download=False)
            
            if not info: return None

            # Lưu ý: Khi dùng extract_flat, cấu trúc JSON có thể gọn hơn
            video_data = {
                'id': info.get('id'),
                'title': info.get('title'),
                'uploader': info.get('uploader'),
                'view_count': info.get('view_count'),
                'duration': info.get('duration'),
                'upload_date': info.get('upload_date'),
                'description': info.get('description'), # Vẫn lấy được description
                'webpage_url': info.get('webpage_url')
            }
            
            print(f"⏱️ Thời gian xử lý: {time.time() - start_time:.2f} giây")
            return video_data

    except Exception as e:
        print(f"Lỗi: {e}")
        return None

# --- Test ---
if __name__ == "__main__":
    url = input("Nhập link video: ").strip()
    if url:
        data = get_quick_metadata(url)
        if data:
            print(f"\nTiêu đề: {data['title']}")
            print(f"Mô tả (100 ký tự đầu): {data['description'][:100]}...")