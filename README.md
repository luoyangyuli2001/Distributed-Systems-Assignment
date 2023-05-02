# Live Video Streaming Service with Facial Recognition 
This application uses Flask and Socket io to create a server and waitress to allow multi-threading on the application. It uses the face_recognition package along with OpenCV to perform facial recognition on images provided in the faceImages folder.

Dependencies that need to be installed:
```
pip3 install numpy
pip3 install opencv-python
pip3 install Flask
pip3 install Flask-SocketIO
pip3 install socketio
pip3 install waitress
pip3 install cmake
pip3 install dlib
pip3 install face_recognition
```

It should be noted that you need to install CMake and C++ environment before you install the dlib package.

After installing all packages, type `python server.py` to start the application.

Navigate to `http://localhost:8080` or the link given by the console.

My demo video link: https://youtu.be/jfiDXDVw7nI