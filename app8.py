import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def analyze_sentiment(text):
    '''
    Function to analyze the sentiment of the transcribed text
    '''
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'Positive'
    elif sentiment < 0:
        return 'Negative'
    else:
        return 'Neutral'

def highlight_keywords(text, keywords):
    '''
    Function to highlight specific keywords in the transcribed text
    '''
    formatted_text = text
    for keyword in keywords:
        formatted_text = formatted_text.replace(keyword, f"<span style='background-color: yellow;'>{keyword}</span>")
    return formatted_text

def generate_wordcloud(text):
    '''
    Function to generate a word cloud from the transcribed text
    '''
    if not text:
        st.warning("Please speak into the microphone to generate a word cloud.")
        return
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(text)
    # plt.figure(figsize=(8,8), facecolor=None)
    # plt.imshow(wordcloud)
    # plt.axis('off')
    # plt.tight_layout(pad=0)
    # st.pyplot()
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    st.pyplot(fig)

def app():
    # Set the title of the app
    st.title("Real-time Speech to Text with Sentiment Analysis and Word Cloud")

    # Initialize the recognizer
    r = sr.Recognizer()

    # Get the user's chosen keywords to highlight
    keywords_input = st.text_input("Enter keywords to highlight (comma-separated):")
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

    # Continuously listen for audio input
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            recording = st.button("Start recording")
        with col2:
            stop = st.button("Stop recording")

    if recording:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            # Adjust the microphone sensitivity
            r.adjust_for_ambient_noise(source)

            # Prompt the user to speak
            st.write("Speak now...")

            text = ''

            # Continuously listen for audio input until the Stop button is pressed
            while not stop:
                # Listen for audio input
                audio = r.listen(source)

                # Use the speech recognition library to transcribe the audio
                try:
                    transcription = r.recognize_google(audio)
                    text += transcription
                    formatted_text = highlight_keywords(text, keywords)
                    st.write(f"Transcription: {formatted_text}", unsafe_allow_html=True)
                    sentiment = analyze_sentiment(text)
                    st.write(f"Sentiment: {sentiment}")
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    st.write(f"Sorry, there was an error processing your request: {e}")
            # Generate a word cloud from the transcribed text
            generate_wordcloud(text)

if __name__ == "__main__":
    app()