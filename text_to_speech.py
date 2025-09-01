import os
# import elevenlabs
# from elevenlabs.client import ElevenLabs
import subprocess
import platform
from pydub import AudioSegment

# ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")


# def text_to_speech_with_elevenlabs(input_text, output_filepath):
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.text_to_speech.convert(
#         text= input_text,
#         voice_id="ZF6FPAbjXT4488VcRRnw", #"JBFqnCBsd6RMkjVDRZzb",
#         model_id="eleven_multilingual_v2",
#         output_format= "mp3_22050_32",
#     )
#     elevenlabs.save(audio, output_filepath)

#     wav_filepath = "final.wav"
#     audio = AudioSegment.from_mp3(output_filepath)
#     audio.export(wav_filepath, format="wav")
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")


from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"



    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    wav_filepath = "/tmp/final.wav"
    audio = AudioSegment.from_mp3(output_filepath)
    audio.export(wav_filepath, format="wav")

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', wav_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# input_text = "Hi, I am Haris"
# output_filepath = "test_text_to_speech.mp3"
# #text_to_speech_with_elevenlabs(input_text, output_filepath)
# text_to_speech_with_gtts(input_text, output_filepath)
