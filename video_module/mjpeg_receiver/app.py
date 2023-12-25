import cv2
import numpy as np
import requests
import os
from openai import OpenAI
import base64
import time
import ffmpeg


os.environ['OPENAI_API_KEY'] = 'YOUR_KEY_HERE'

client = OpenAI()


# MJPEG-streamer URL
stream_url = "http://127.0.0.1:5000/video"

# Open a connection to the stream
stream = requests.get(stream_url, stream=True)

# Prepare to capture frames
video_duration = 30  # desired video duration in seconds
fps = 30  # frames per second
frame_count = video_duration * fps
frames = []

# Read and store frames
bytes = b''
for frame in range(frame_count):
    for chunk in stream.iter_content(chunk_size=1024):
        bytes += chunk
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is not None:
                # Extract dimensions from the first frame
                if len(frames) == 0:
                    height, width = frame.shape[:2]

                frames.append(frame)
                break

# Release the stream
stream.close()

# Check if frames were captured
if len(frames) > 0:
    # Create a video from frames
    video_filename = 'output.mp4'
    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for frame in frames:
        out.write(frame)

    # Release the video writer
    out.release()
else:
    print("No frames captured from the stream.")


if video_filename:
    video = cv2.VideoCapture("output.mp4")

    base64Frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    video.release()
    print(len(base64Frames), "frames read.")

    # input_file = 'output.mp4'
    # output_file = 'output.mp3'

    # ffmpeg.input(input_file).output(output_file).run()


    # audio_file = open("output.mp4", "rb")
    # transcript = client.audio.transcriptions.create(
    # model="whisper-1",
    # file=audio_file,
    # response_format="text"
    # )

    # print(transcript)

    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                f"""From the frames of the input video you should decsribe the content of the sequential frames altogether. Donot describe each frame individually, but describe altogether as a scene. You are like a robot with a camera input(assume the frames as the input) """,
                *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
            ],
        }
    ]

    params = {
        "model": "gpt-4-vision-preview",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 100,
    }

    result = client.chat.completions.create(**params)
    print(result.choices[0].message.content)


