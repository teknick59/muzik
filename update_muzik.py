import os
import requests
import xmltodict

API_KEY = os.getenv("YT_API_KEY_MUZIK")
CHANNEL_FILE = "data/muzik.txt"
XML_PATH = "xml/muzik.xml"


def read_channels(path):
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ids.append(line.split()[0])
    return ids


def get_videos(channel_id, event_type):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&channelId={channel_id}&eventType={event_type}&type=video&key={API_KEY}"
    )
    r = requests.get(url)
    data = r.json()

    results = []
    for item in data.get("items", []):
        vid = item["id"]["videoId"]
        title = item["snippet"]["title"]
        thumb = item["snippet"]["thumbnails"]["high"]["url"]
        results.append({
            "title": title,
            "thumb": thumb,
            "type": "youtube",
            "src": vid
        })
    return results


def main():
    channels = read_channels(CHANNEL_FILE)
    media_items = []

    for cid in channels:
        live_videos = get_videos(cid.strip(), "live")
        upcoming_videos = get_videos(cid.strip(), "upcoming")
        media_items += live_videos + upcoming_videos

    if not media_items:
        media_items = [{
            "title": "No live or upcoming videos",
            "thumb": "",
            "type": "info",
            "src": ""
        }]

    xml_data = {"media": {"media": media_items}}
    xml_str = xmltodict.unparse(xml_data, pretty=True)

    os.makedirs(os.path.dirname(XML_PATH), exist_ok=True)
    with open(XML_PATH, "w", encoding="utf-8") as f:
        f.write(xml_str)


if __name__ == "__main__":
    main()
