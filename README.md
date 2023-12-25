# Voice-command-classification
Classifying voice command to one of the four classes (FORWARD, BACKWARD, RIGHT, LEFT) for robot navigation.


## ROBOT SCENE DESCRIPTION MODULE

There are two different files:
   - mjpeg_streamer [`python app.py` will turn on a flask streaming app, on the url `http://127.0.0.1:5000/video`]

   - mjpeg_receiver [`python app.py` will turn on a video description module which will describe the whole input scene]

   - ## REPLACE THE OPENAI_KEY in the receiver app (make sure that the account has the GPT-4 VISION enabled)
