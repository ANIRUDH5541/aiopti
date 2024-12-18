from pytube import YouTube
import pytesseract
from PIL import Image
import openai
from youtube_transcript_api import YouTubeTranscriptApi

openai.api_key = 'your-openai-api-key'

def get_youtube_text(url):
    yt = YouTube(url)
    if yt.captions:
        captions = yt.captions.get_by_language_code('en')
        return captions.generate_srt_captions()
    else:
        print("No subtitles found. You may need to process the video frames.")
def get_video_id(url):
    # Extracts the video ID from the URL
    video_id = url.split('v=')[1].split('&')[0]
    return video_id

def get_video_text(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def summarize_video(text):
    """Summarize the video content using OpenAI's API."""
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose other models if needed
        prompt=f"Summarize the following content: {text}",
        max_tokens=200  # Control the length of the summary
    )
    return response.choices[0].text.strip()

def get_video_summary(video_url):
    """Retrieve and summarize YouTube video content."""
    yt = YouTube(video_url)
    if yt.captions:
        captions = yt.captions.get_by_language_code('en')
        caption_text = captions.generate_srt_captions()
        summary = summarize_video(caption_text)
        return summary
    else:
        return "No subtitles available to summarize."

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=example"
    print(get_youtube_text(video_url))
