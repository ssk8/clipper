import yt_dlp
import qbittorrentapi
from os import environ


tbox_address = "http://192.168.1.106"


def dl_vids(vid_list, ydl_opts={}):
    clean_vid_list = []
    for vid in vid_list:
        if "watch?v=" in vid:
            start = vid.find("watch?v=") + 8
        else:
            start = vid.rfind("/") + 1
        clean = vid[start : start + 11]
        print(vid, clean)
        clean_vid_list.append(clean)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(clean_vid_list)
        print(f"getting {clean_vid_list}")


def add_torrents(links_list):
    print("attempting to send:\n")
    print(links_list)
    qb = qbittorrentapi.Client(
        host=tbox_address,
        port=8080,
        username=environ["QBIT_NAME"],
        password=environ["QBIT_PW"],
    )
    qb.auth_log_in()
    qb.torrents_add(urls=links_list)
    print(f"sent {len(links_list)} torrents to {tbox_address}")


def write_to_file(text):
    with open("/home/curt/clips.txt", "a") as clips_file:
        clips_file.write(text + "\n")
