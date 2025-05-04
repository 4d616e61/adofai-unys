#import yt_dlp
import json5
import json
import sys  
import codecs
import yaml
import subprocess
import requests
import os


c_ytdlp_release_url = "https://github.com/yt-dlp/yt-dlp/releases/download/2025.04.30/yt-dlp.exe"
c_ytdlp_executable = "./bin/yt-dlp.exe"
c_ffmpeg_executable = "./bin/ffmpeg.exe"
c_out_audio = "audio.wav"
# ydl_opts = {
#     'format': 'm4a/bestaudio/best',
#     # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#     'postprocessors': [{  # Extract audio using ffmpeg
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'wav',
#     }]
# }

#i really hate windose programming :((
def check_or_download_ytdlp():
    if os.path.exists(c_ytdlp_executable):
        return
    os.makedirs("bin", exist_ok=True)
    print("downloading ytdlp since it doesnt exist")
    resp = requests.get(c_ytdlp_release_url, allow_redirects=True)
    cont = resp.content
    with open(c_ytdlp_executable, "wb") as f:
        f.write(cont)


def download_audio(url):
    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     error_code = ydl.download([ys_url])
    # print(error_code)
    check_or_download_ytdlp()
    subprocess.run([c_ytdlp_executable, url, "--extract-audio", "--audio-format", "wav", "-o", c_out_audio])

def load_adofai_file(fname):
    with open(fname, "rb") as f:
        bom_maybe = f.read(3)
        if bom_maybe != codecs.BOM_UTF8:
            print(bom_maybe)
            f.seek(0)
        cont = f.read()

        level = json5.loads(cont)
        return level

def main():
    if len(sys.argv) < 2:
        level_fname = "level.adofai"
    else:
        level_fname = sys.argv[1]
    out_fname = "no_ys_" + level_fname
    level_obj = load_adofai_file(level_fname)
    level_settings = level_obj["settings"]
    #print(level_obj)
    if (not "requiredMods" in level_settings.keys()) or (not "songURL" in level_settings.keys()) :
        print("Not YSMod level. Exiting...")
        return
    del level_settings["requiredMods"]
    ys_url = level_settings["songURL"]
    del level_settings["songURL"]
    download_audio(ys_url)
    level_settings["songFilename"] = c_out_audio


    with open(out_fname, "w") as f:
        f.write(json.dumps(level_obj, indent=3))


if __name__ == "__main__":
    main()