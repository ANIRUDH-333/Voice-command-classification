from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames('file_example_MP4_480_1_5MG.mp4'), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
