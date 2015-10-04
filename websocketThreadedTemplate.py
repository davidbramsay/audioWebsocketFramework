from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import threading
from Queue import Queue
import time


#websocket server and static file server

app = Flask(__name__) 


inQueue = Queue(maxsize=10) #handle incoming websocket commands
outQueue = Queue(maxsize=10) #handle outgoing websocket view updates


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def style(path):
    print path
    return app.send_static_file(path)

@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            inQueue.put(ws.receive())
            ws.send(outQueue.get())
    return


#bridge websockets to audio functions

def do_something(int1, int2):
	return int1+int2


#audio functions

def main_audio_thread(arg1, stop_event):
    while (not stop_event.is_set()):
        if (not inQueue.empty()):
            message = inQueue.get()
            if message is not None:
                print message + str(len(message))
            if(message=="quit"):
                print "QUIT MESSAGE"
                stop_event.set()
            outQueue.put("success")
        else:
            print "TESTING"
            time.sleep(.2)
        pass

#start each thread

def main_web_thread():
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
     

if __name__ == '__main__':

    threads = []

    thread = threading.Thread(target=main_web_thread)
    thread.daemon = True
    thread.start()
    threads.append(thread)
  
    audiothread_stop = threading.Event()
    thread = threading.Thread(target=main_audio_thread, args=(2, audiothread_stop))
    thread.start()
    threads.append(thread)

    #audiothread_stop.wait()
    #print "final quit event"
