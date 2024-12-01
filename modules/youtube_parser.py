from pytube import YouTube
import pytesseract
from PIL import Image

def get_youtube_text(url):
    yt = YouTube(url)
    if yt.captions:
        captions = yt.captions.get_by_language_code('en')
        return captions.generate_srt_captions()
    else:
        print("No subtitles found. You may need to process the video frames.")

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=example"
    print(get_youtube_text(video_url))
