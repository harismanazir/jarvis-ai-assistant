# import os
# import gradio as gr
# from speech_to_text import record_audio, transcribe_with_groq
# from ai_agent import ask_agent
# # from text_to_speech import text_to_speech_with_elevenlabs, text_to_speech_with_gtts
# from text_to_speech import text_to_speech_with_gtts

# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# audio_filepath = "audio_question.mp3"


# def process_audio_and_chat():
#     chat_history = []
#     while True:
#         try:
#             record_audio(file_path=audio_filepath)
#             user_input = transcribe_with_groq(audio_filepath)

#             if "goodbye" in user_input.lower():
#                 break

#             response = ask_agent(user_query=user_input)

#             voice_of_doctor = text_to_speech_with_gtts(input_text=response, output_filepath="final.mp3")

#             chat_history.append([user_input, response])

#             yield chat_history

#         except Exception as e:
#             print(f"Error in continuous recording: {e}")
#             break

# # Code for frontend
# import cv2
# # Global variables
# camera = None
# is_running = False
# last_frame = None

# def initialize_camera():
#     """Initialize the camera with optimized settings"""
#     global camera
#     if camera is None:
#         camera = cv2.VideoCapture(0)
#         if camera.isOpened():
#             # Optimize camera settings for better performance
#             camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#             camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#             camera.set(cv2.CAP_PROP_FPS, 30)
#             camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to minimize lag
#     return camera is not None and camera.isOpened()

# def start_webcam():
#     """Start the webcam feed"""
#     global is_running, last_frame
#     is_running = True
#     if not initialize_camera():
#         return None
    
#     ret, frame = camera.read()
#     if ret and frame is not None:
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         last_frame = frame
#         return frame
#     return last_frame

# def stop_webcam():
#     """Stop the webcam feed"""
#     global is_running, camera
#     is_running = False
#     if camera is not None:
#         camera.release()
#         camera = None
#     return None

# def get_webcam_frame():
#     """Get current webcam frame with optimized performance"""
#     global camera, is_running, last_frame
    
#     if not is_running or camera is None:
#         return last_frame
    
#     # Skip frames if buffer is full to avoid lag
#     if camera.get(cv2.CAP_PROP_BUFFERSIZE) > 1:
#         for _ in range(int(camera.get(cv2.CAP_PROP_BUFFERSIZE)) - 1):
#             camera.read()
    
#     ret, frame = camera.read()
#     if ret and frame is not None:
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         last_frame = frame
#         return frame
#     return last_frame

# # Setup UI

# with gr.Blocks() as demo:
#     gr.Markdown("<h1 style='color: orange; text-align: center;  font-size: 4em;'> 👧🏼 Jarvis – Your Personal AI Assistant</h1>")

#     with gr.Row():
#         # Left column - Webcam
#         with gr.Column(scale=1):
#             gr.Markdown("## Webcam Feed")
            
#             with gr.Row():
#                 start_btn = gr.Button("Start Camera", variant="primary")
#                 stop_btn = gr.Button("Stop Camera", variant="secondary")
            
#             webcam_output = gr.Image(
#                 label="Live Feed",
#                 streaming=True,
#                 show_label=False,
#                 width=640,
#                 height=480
#             )
            
#             # Faster refresh rate for smoother video
#             webcam_timer = gr.Timer(0.033)  # ~30 FPS (1/30 ≈ 0.033 seconds)
        
#         # Right column - Chat
#         with gr.Column(scale=1):
#             gr.Markdown("## Chat Interface")
            
#             chatbot = gr.Chatbot(
#                 label="Conversation",
#                 height=400,
#                 show_label=False
#             )
            
#             gr.Markdown("*🎤 Continuous listening mode is active - speak anytime!*")
            
#             with gr.Row():
#                 clear_btn = gr.Button("Clear Chat", variant="secondary")
    
#     # Event handlers
#     start_btn.click(
#         fn=start_webcam,
#         outputs=webcam_output
#     )
    
#     stop_btn.click(
#         fn=stop_webcam,
#         outputs=webcam_output
#     )
    
#     webcam_timer.tick(
#         fn=get_webcam_frame,
#         outputs=webcam_output,
#         show_progress=False  # Hide progress indicator for smoother experience
#     )
    
#     clear_btn.click(
#         fn=lambda: [],
#         outputs=chatbot
#     )
    
#     # Auto-start continuous mode when the app loads
#     demo.load(
#         fn=process_audio_and_chat,
#         outputs=chatbot
#     )

# ## Launch the app
# if __name__ == "__main__":
#     demo.launch(
#         server_name="0.0.0.0",
#         server_port=7860,
#         share=True,
#         debug=True
#     )

import os
import gradio as gr
import cv2
from speech_to_text import record_audio, transcribe_with_groq
from ai_agent import ask_agent
from text_to_speech import text_to_speech_with_gtts
import app_globals

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
audio_filepath = "audio_question.mp3"

# Global state variables
chat_history = []
is_listening = True  # Default: listening mode ON
camera = None
is_running = False
last_frame = None

# ----------------- AI Audio & Chat Logic -----------------
def process_audio_and_chat():
    global chat_history, is_listening

    while True:
        try:
            if not is_listening:
                # If paused, just yield existing chat without recording/transcribing
                yield chat_history
                continue

            # Record and transcribe only if listening
            record_audio(file_path=audio_filepath)
            user_input = transcribe_with_groq(audio_filepath)

            response = ask_agent(user_query=user_input)
            voice_of_doctor = text_to_speech_with_gtts(
                input_text=response,
                output_filepath="final.mp3",
                play_locally=False  # Must be False for Render
            )

            chat_history.append([user_input, response])

            yield chat_history, voice_of_doctor

        except Exception as e:
            print(f"Error in continuous recording: {e}")
            break


def record_and_ask(chat_history):
    try:
        ask_btn.value = "🎙 Recording..."
        ask_btn.interactive = False

        # Step 1: Record audio
        record_audio(file_path=audio_filepath)

        # Step 2: Transcribe audio
        user_input = transcribe_with_groq(audio_filepath)

        if not user_input.strip():
            ask_btn.value = "🎤 Ask Question"
            ask_btn.interactive = True
            return chat_history, None

        # Step 3: Get AI response
        response = ask_agent(user_query=user_input)

        # Step 4: Convert AI response to speech
        voice_of_doctor = text_to_speech_with_gtts(
            input_text=response,
            output_filepath="final.mp3",
            play_locally=False
        )

        # Step 5: Update chat
        chat_history.append([user_input, response])

        ask_btn.value = "🎤 Ask Question"
        ask_btn.interactive = True

        return chat_history, voice_of_doctor

    except Exception as e:
        print(f"Error in record_and_ask: {e}")
        ask_btn.value = "🎤 Ask Question"
        ask_btn.interactive = True
        return chat_history, None

# ----------------- Pause & Resume Listening -----------------
def pause_listening():
    global is_listening
    is_listening = False
    return chat_history

def resume_listening():
    global is_listening
    is_listening = True
    return chat_history
def clear_chat():
    global chat_history
    chat_history = []   # Reset stored history
    return []



# ----------------- Webcam Logic -----------------
def initialize_camera():
    """Initialize the camera with optimized settings"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if camera.isOpened():
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            camera.set(cv2.CAP_PROP_FPS, 30)
            camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return camera is not None and camera.isOpened()

def start_webcam():
    """Start the webcam feed"""
    global is_running, last_frame
    is_running = True
    if not initialize_camera():
        return None

    ret, frame = camera.read()
    if ret and frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        last_frame = frame
        return frame
    return last_frame




 
# def stop_webcam():
#     """Stop the webcam feed"""
#     global is_running, camera
#     is_running = False
#     if camera is not None:
#         camera.release()
#         camera = None
#     return None

def stop_webcam():
    global camera, is_running
    is_running = False
    last_frame = None
    if camera is not None and camera.isOpened():
        camera.release()
        camera = None
    return None


# def get_webcam_frame():
#     """Get current webcam frame with optimized performance"""
#     global camera, is_running, last_frame

#     if not is_running or camera is None:
#         return last_frame

#     # Flush the buffer to prevent lag
#     if camera.get(cv2.CAP_PROP_BUFFERSIZE) > 1:
#         for _ in range(int(camera.get(cv2.CAP_PROP_BUFFERSIZE)) - 1):
#             camera.read()

#     ret, frame = camera.read()
#     if ret and frame is not None:
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         app_globals.last_frame = frame.copy()  # FORCE a fresh copy for Gradio
#         return app_globals.last_frame
#     return app_globals.last_frame




def get_webcam_frame():
    global camera, is_running, last_frame

    if not is_running or camera is None or not camera.isOpened():
        return None

    ret, frame = camera.read()

    # If camera fails, return last good frame
    if not ret or frame is None:
        return None

    # Convert BGR → RGB for display
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    last_frame = frame.copy()
    app_globals.last_frame = last_frame.copy()

    return last_frame



# ----------------- Gradio UI -----------------
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='color: orange; text-align: center;  font-size: 4em;'> 👧🏼 Jarvis – Your Personal AI Assistant</h1>")

    with gr.Row():
        # Left column - Webcam
        with gr.Column(scale=1):
            gr.Markdown("## Webcam Feed")

            with gr.Row():
                start_btn = gr.Button("Start Camera", variant="primary")
                stop_btn = gr.Button("Stop Camera", variant="secondary")

            webcam_output = gr.Image(
                label="Live Feed",
                streaming=True,
                show_label=False,
                width=640,
                height=480,
                type="numpy"  # Ensure numpy array format for better performance
            )

            # ✅ Correct way for latest Gradio
            webcam_timer = gr.Timer(value=0.033)
            webcam_timer.tick(fn=get_webcam_frame, outputs=webcam_output, show_progress=False)

            



        # Right column - Chat
        with gr.Column(scale=1):
            gr.Markdown("## Chat Interface")

            chatbot = gr.Chatbot(
                label="Conversation",
                height=400,
                show_label=False
            )
            audio_output = gr.Audio(
                label="🔊 AI Voice",
                autoplay=True,
                type="filepath",  # Important: Gradio will play the file automatically
                interactive=False
            )
            gr.Markdown("*🎤 Continuous listening mode is active - speak anytime!*")

            with gr.Row():
                ask_btn = gr.Button("🎤 Ask Question", variant="primary")

                # pause_btn = gr.Button("⏸️ Pause Listening", variant="secondary")
                # resume_btn = gr.Button("▶️ Resume Listening", variant="primary")
                clear_btn = gr.Button("Clear Chat", variant="secondary")
    
    
    # Event handlers
    start_btn.click(fn=start_webcam, outputs=webcam_output)
    stop_btn.click(fn=stop_webcam, outputs=webcam_output)
    webcam_timer.tick(fn=get_webcam_frame, outputs=webcam_output, show_progress=False)
    ask_btn.click(
    fn=record_and_ask,
    inputs=chatbot,
    outputs=[chatbot, audio_output]
)

    # pause_btn.click(fn=pause_listening, outputs=chatbot)
    # resume_btn.click(fn=resume_listening, outputs=chatbot)
   
    clear_btn.click(fn=clear_chat,outputs=chatbot)


    # demo.load(fn=process_audio_and_chat, outputs=[chatbot, audio_output])

# ----------------- Launch the App -----------------
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    )
