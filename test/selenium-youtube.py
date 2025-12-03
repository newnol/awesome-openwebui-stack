from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

def get_info_via_js_variable(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"🔄 Đang truy cập: {url}")
        driver.get(url)

        # --- KEY TECHNIQUE: Trích xuất biến JS ---
        # YouTube lưu mọi info trong biến object: ytInitialPlayerResponse
        # Ta dùng Selenium execute_script để return biến đó về Python
        player_data = driver.execute_script("return ytInitialPlayerResponse;")

        if not player_data:
            return None

        # Parse dữ liệu JSON (Không cần đụng vào HTML/CSS)
        video_details = player_data.get('videoDetails', {})
        
        title = video_details.get('title')
        # Description ở đây luôn là FULL TEXT (không bị cắt)
        description = video_details.get('shortDescription') 
        
        return {
            "title": title,
            "description": description
        }

    except Exception as e:
        print(f"Lỗi: {e}")
        return None
    finally:
        driver.quit()

# --- Test ---
if __name__ == "__main__":
    link = "https://www.youtube.com/watch?v=r-oGDUZ33I0"
    data = get_info_via_js_variable(link)
    
    if data:
        print("-" * 30)
        print(f"Title: {data['title']}")
        print("-" * 30)
        print("Description Full (Lấy trực tiếp từ biến JS):")
        print(data['description'])