import random
import time
import requests

URL = "https://api.openwebui.com/api/v1/tools/id/a2863c56-d3b0-4238-883c-941a569cd0d6/download"

# Một vài user agent phổ biến (bạn có thể thêm/bớt tuỳ ý)
USER_AGENTS = [
    # Chrome trên macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Chrome trên Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]

# Có thể map kèm theo sec-ch-ua tương ứng nếu muốn “thật” hơn
SEC_CH_UA_LIST = [
    '"Chromium";v="142", "Brave";v="142", "Not_A Brand";v="99"',
    '"Google Chrome";v="121", "Not(A:Brand";v="8", "Chromium";v="121"',
    '"Google Chrome";v="120", "Not.A/Brand";v="24", "Chromium";v="120"',
]

def main():
    for i in range(100):
        ua = random.choice(USER_AGENTS)
        sec_ch_ua = random.choice(SEC_CH_UA_LIST)

        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://openwebui.com",
            "Referer": "https://openwebui.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "User-Agent": ua,
            "sec-ch-ua": sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            'sec-ch-ua-platform': '"macOS"',
        }

        print(f"[{i+1}/30] Gửi request với UA: {ua}")
        try:
            resp = requests.get(URL, headers=headers, timeout=30)
            print(f"  -> Status code: {resp.status_code}")
            # Nếu là file download, có thể ghi ra file:
            # with open(f"download_{i+1}.bin", "wb") as f:
            #     f.write(resp.content)
        except Exception as e:
            print(f"  -> Lỗi: {e}")

        # Nghỉ một chút để trông “tự nhiên” hơn
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    main()