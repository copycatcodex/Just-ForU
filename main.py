import requests
import time
from config import token
import os

# Function untuk mendapatkan informasi user
def get_info(token):
    url_info = 'https://api.foruai.io/v1/user/profile'
    headers = {
        "authority": "api.foruai.io",
        "method": "GET",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f'Bearer {token}',  
        "origin": "https://foruai.io",
        "referer": "https://foruai.io/",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127", "Microsoft Edge WebView2";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "x-foru-apikey": "foru-private-aec4199767b805b22ce88a2399ea7730d998e5caff336fda19acb897cd9d47e2",
        "x-foru-signature": "8005df48001ba38406ae9544645ac2813a201b68c04ee765580e9a696578c03c",
        "x-foru-timestamp": "1726762687536",
    }

    try:
        response = requests.get(url_info, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get('code') == 200:
            user = data.get('data', {})
            nama = user.get('name', 'N/A')
            level = user.get('level', 0)
            playpass = user.get('playpass', 0)
            stat_us = user.get('status', 0)
            info_string = f"Nama: {nama} | level: {level} | playpass: {playpass} | status: {stat_us}"
            print(info_string)
            return info_string, user
        else:
            print(f"Gagal mengambil data user, code: {data.get('code')}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan: {e}")
        return None, None

# Function untuk mengirim click
def execute_click(token):
    url_click = 'https://api.foruai.io/v1/shake/process'
    headers = {
        'authority': 'api.foruai.io',
        'method': 'POST',
        'path': '/v1/shake/process',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',  
        'content-length': '29',
        'content-type': 'application/json',
        'origin': 'https://foruai.io',
        'priority': 'u=1, i',
        'referer': 'https://foruai.io/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127", "Microsoft Edge WebView2";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-foru-apikey': 'foru-private-aec4199767b805b22ce88a2399ea7730d998e5caff336fda19acb897cd9d47e2',
        'x-foru-signature': '27edc9dd46dd2a289b2e22f651959c85f16adc53f67dffc9a57280c37ce4539e',
        'x-foru-timestamp': '1726765910485',
    }

    try:
        response = requests.post(url_click, headers=headers, json={})
        response.raise_for_status()
        data = response.json()

        if data.get('code') == 201:
            return {
                "success": True,
                "point_settle": data['data']['point_settle'],
                "point_pending": data['data']['point_pending']
            }
        else:
            return {"success": False, "message": data}

    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat mengirimkan permintaan: {e}")
        return {"success": False, "message": str(e)}

try:
    #
    
    info_string, user = get_info(token)
    banner = "===== JUSTFORU ====="
    
    if user:
        while True:
            print("\033c", end="") 
            print(banner)
            print(info_string)  
            
            
            result = execute_click(token)
            if result['success']:
                print(f"Point settle: {result['point_settle']} | Point pending: {result['point_pending']} | Sukses: success")
            else:
                print(f"Gagal klik. Pesan: {result['message']}")
            
            time.sleep(0.3)  # Jeda antara klik
except KeyboardInterrupt:
    print("\nProses dihentikan oleh pengguna.")
