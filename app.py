import streamlit as st
import requests
import zipfile
import io

st.title("Interview → ElevenLabs Audio Generator")

api_key = st.text_input("ElevenLabs API key", type="password")
voice_id = st.text_input("Voice ID")

text = st.text_area("Paste your interview text")

generate = st.button("Generate audio")

def split_blocks(text):
    blocks = []
    current = []
    for line in text.split("\n"):
        if line.strip() == "":
            if current:
                blocks.append(" ".join(current))
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(" ".join(current))
    return blocks

if generate:

    blocks = split_blocks(text)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    zip_buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, "w")

    for i, block in enumerate(blocks):

        data = {
            "text": block,
            "model_id": "eleven_multilingual_v2"
        }

        r = requests.post(url, json=data, headers=headers)

        filename = f"audio_{i+1}.mp3"

        zip_file.writestr(filename, r.content)

    zip_file.close()

    st.download_button(
        label="Download ZIP",
        data=zip_buffer.getvalue(),
        file_name="interview_audio.zip"
    )
