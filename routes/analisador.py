import os
from dotenv import load_dotenv
from groq import Groq
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, render_template, Blueprint

analisador = Blueprint('analisador', __name__)

@analisador.route('/')
def index():
    return render_template('index.html')

@analisador.route('/analise', methods=['POST'])
def submit():
    video_url = request.form['user_input'] 

    try:
        parsed_url = urlparse(video_url)

        if "youtu.be" in parsed_url.netloc:
            video_id = parsed_url.path[1:]
        else:
            query = parse_qs(parsed_url.query)
            video_id = query.get("v")

            if not video_id:
                raise ValueError("ID do vídeo não pôde ser extraído.")

            video_id = video_id[0]

        available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        print("Idiomas disponíveis para transcrição:")
        for transcript in available_transcripts:
            print(transcript.language)

            transcripts = available_transcripts.find_transcript(['pt'])
            subtitle_text = " ".join([entry["text"] for entry in transcripts.fetch()])

            texto = subtitle_text

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

    load_dotenv()

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Você é um assitente que resume videos detalhadamente, Responda com formatação Markdown",
            },

            {
                "role": "user",
                "content": f"Descreva o seguinte video: {texto}",
            }
        ],
        model="llama3-8b-8192",
    )

    analise = chat_completion.choices[0].message.content
    return render_template('index.html', analise=analise)