import gradio as gr
from openai import OpenAI
import io
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API = os.getenv("OPEN_AI_API")
voices: list[str] = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def generate_speech(api_key: str = "", voice: str = "onyx", speech_rate: float = 1.00, input_text: str = ""):
    if not input_text or len(input_text) <= 5:
        return

    if api_key is None:
        return "Please provide a valid OpenAI API key"

    client = OpenAI(api_key=api_key)

    speech = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=input_text,
        speed=speech_rate
    )

    buffer = io.BytesIO()
    for chunk in speech.iter_bytes(chunk_size=4096):
        buffer.write(chunk)

    buffer.seek(0)

    return buffer.read()


with gr.Blocks() as app:
    tti = gr.Interface(

    )
    tts = gr.Interface(
        fn=generate_speech,
        inputs=[
            gr.Textbox(label="Your OPENAI API Key", lines=1, type="password"),
            gr.Dropdown(label="Choose Voice",
                        info="This will be the voice of your speech",
                        choices=voices,
                        show_label=True,
                        value="onyx"
                        ),
            # gr.Slider(label="Control the speech rate",
            #           minimum=0.25,
            #           maximum=4.0,
            #           step=0.25,
            #           value=1.00,
            #           visible=False),
            gr.Textbox(label="Your text goes here", lines=3)
        ],
        outputs=gr.Audio(label="Speech",
                         show_label=True,
                         format="wav",
                         show_download_button=True,
                         type="numpy",
                         ),
        title="Text to Speech",
        description="Convert your text to speech in a few seconds",
        api_name="OpenAI",
        allow_flagging=None,
    )

if __name__ == "__main__":
    print("just:main")
    app.launch(share=False, debug=False)
