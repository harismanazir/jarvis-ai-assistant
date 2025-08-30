import cv2
import base64
from dotenv import load_dotenv
import time
import app_globals

load_dotenv()


def capture_image():
    frame = app_globals.last_frame 
    if frame is None:
        raise RuntimeError("No frame available. Start the camera first.")

    # Encode frame as JPEG
    ret, buffer = cv2.imencode(".jpg", frame)
    if not ret:
        raise RuntimeError("Failed to encode frame.")

    # Return as base64 string if needed
    return base64.b64encode(buffer).decode("utf-8")



# def capture_image() -> str:
#     """
#     Captures one frame from the default webcam, resizes it,
#     encodes it as Base64 JPEG (raw string) and returns it.
#     """
#     for idx in range(10):
#         # cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
#         cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)   # Windows recommended backend

#         if cap.isOpened():
#             time.sleep(3)
#             for _ in range(10):  # Warm up
#                 cap.read()
#             ret, frame = cap.read()
#             cap.release()
#             if not ret:
#                 continue
#             # cv2.imwrite("sample.jpg", frame)  # Optional
#             ret, buf = cv2.imencode('.jpg', frame)
#             if ret:
#                 return base64.b64encode(buf).decode('utf-8')
#     raise RuntimeError("Could not open any webcam (tried indices 0-3)")



from groq import Groq

def analyze_image_with_query(query: str) -> str:
    """
    Expects a string with 'query'.
    Captures the image and sends the query and the image to
    to Groq's vision chat API and returns the analysis.
    """
    img_b64 = capture_image()
    model="meta-llama/llama-4-maverick-17b-128e-instruct"
    
    if not query or not img_b64:
        return "Error: both 'query' and 'image' fields required."

    client=Groq()  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_b64}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )
    
    return chat_completion.choices[0].message.content

# query = "what is in the hand of the guy ?"
# print(analyze_image_with_query(query))
