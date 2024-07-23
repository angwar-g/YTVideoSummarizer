import streamlit as st
from dotenv import load_dotenv
load_dotenv()   # load environment variables from .env file
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = '''You are a YouTube video summarizer. 
You will be taking the transcript the transcript text of a video, 
summarizing the entire video and providing the important summary of the video in bullet points in around 200-300 words. 
The transcript text is as follows: '''

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    
    try:
        return response.text
    except Exception as e:
        return "Failed to generate a response due to safety concerns or other issues. Please try again with a different video."

def extract_transcript(video_url):
    try:
        video_id = video_url.split('=')[1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
        
    except Exception as e:
        raise e

st.title("YouTube Video Summarizer")
youtube_link = st.text_input("Enter the YouTube video link:")

if youtube_link:
    video_id = youtube_link.split('=')[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize Video"):
    with st.spinner('Extracting transcript and generating summary...'):
        transcript_text = extract_transcript(youtube_link)

        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.write(summary)

    

