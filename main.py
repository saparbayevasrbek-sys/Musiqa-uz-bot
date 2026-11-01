import urllib.request
import urllib.parse
import json
import time
import os

TOKEN = "9166927324:AAFH2ZJwiGREC1c89Tpc3fVgbOD9c_q5VVQ"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    try:
        return json.loads(urllib.request.urlopen(url, timeout=30).read().decode('utf8'))
    except:
        return None

def send_message(chat_id, text):
    try:
        url = URL + f"sendMessage?chat_id={chat_id}&text=" + urllib.parse.quote(text)
        urllib.request.urlopen(url, timeout=15)
    except:
        pass

def send_audio(chat_id, audio_url, title, performer):
    try:
        params = urllib.parse.urlencode({'chat_id': chat_id, 'audio': audio_url, 'title': title, 'performer': performer})
        urllib.request.urlopen(URL + f"sendAudio?{params}", timeout=20)
    except:
        pass

def search_real_music(query):
    try:
        api_url = f"https://itunes.apple.com/search?term={urllib.parse.quote(query)}&entity=song&limit=10"
        data = json.loads(urllib.request.urlopen(api_url, timeout=10).read().decode('utf-8'))
        if data["resultCount"] > 0:
            track = data["results"][0]
            return {"url": track.get("previewUrl"), "title": track.get("trackName"), "performer": track.get("artistName")}
    except:
        pass
    return None

def main():
    print("Bot cloud serverda ishga tushdi...")
    offset = None
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            for item in updates["result"]:
                offset = item["update_id"] + 1
                if "message" in item and "text" in item["message"]:
                    chat_id = item["message"]["chat"]["id"]
                    text = item["message"]["text"]
                    if text == "/start":
                        send_message(chat_id, "Salom! Cloud serverdan ishlayapman. Istalgan qo'shiq nomini yozing.")
                    else:
                        send_message(chat_id, f"'{text}' qidirilmoqda...")
                        found = search_real_music(text)
                        if found and found["url"]:
                            send_audio(chat_id, found["url"], found["title"], found["performer"])
                        else:
                            send_message(chat_id, "Bu qo'shiq topilmadi, boshqasini yozib ko'ring.")
        time.sleep(1)

if __name__ == '__main__':
    main()
