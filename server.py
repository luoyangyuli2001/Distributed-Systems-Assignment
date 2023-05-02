from livevideo import app
from waitress import serve
import socketio
import socket
 
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)  
appServer = socketio.WSGIApp(socketio.Server(), app)

if __name__ == '__main__':
    print("Server started with http://127.0.0.1:8080 or http://"+IPAddr+":8080")
    serve(appServer, host='0.0.0.0', port=8080, url_scheme='http', threads=10)