import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print(f'a new user has connected with sid:{sid}')


@sio.event
def disconnect(sid):
    print(f'user with sid:{sid} has disconnected...')


@sio.on('send_message')
def broadcast_message(sid, message, username, time):
    print(f'user sid:{sid} with username {username} sent message: "{message}" at {time} epochs')
    sio.emit('new_message', (message, username, time))


@sio.on('client_typing')
def broadcast_user_typing(sid, username):
    print(f'user sid:{sid} with username {username} is typing...')
    sio.emit('user_typing', username)


@sio.on('no_client_typing')
def broadcast_user_not_typing(sid, username):
    print(f'user sid:{sid} with username {username} is not typing...')
    sio.emit('user_not_typing', username)


eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 1234)), app)
