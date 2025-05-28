import os
import asyncio
import json
import threading
from flask import Flask, render_template
from flask_sock import Sock
import websockets
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, static_folder='static', static_url_path='/static')
sock = Sock(app)


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = "agent_01jw8z2s6wemv9wv1r143pp1ck" 
ELEVENLABS_WS_URL = f"wss://api.elevenlabs.io/v1/convai/conversation?agent_id={AGENT_ID}"

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@sock.route('/ws')
def audio_websocket(ws):
    """Handles the WebSocket proxy using dedicated threads."""
    
    to_elevenlabs_queue = asyncio.Queue()
    
    def receive_from_frontend():
        while True:
            try:
                message = ws.receive()
                if message:
                    asyncio.run(to_elevenlabs_queue.put(message))
            except Exception as e:
                print(f"Frontend connection closed or error: {e}")
                break

    async def elevenlabs_proxy():
        try:
            async with websockets.connect(ELEVENLABS_WS_URL) as elevenlabs_ws:
                await elevenlabs_ws.send(json.dumps({
                    "xi_api_key": ELEVENLABS_API_KEY,
                    "send_initial_message": True
                }))

                async def forward_to_elevenlabs():
                    while True:
                        message = await to_elevenlabs_queue.get()
                        await elevenlabs_ws.send(message)

                async def forward_to_frontend():
                    while True:
                        response = await elevenlabs_ws.recv()
                        ws.send(response)

                await asyncio.gather(forward_to_elevenlabs(), forward_to_frontend())
        except Exception as e:
            print(f"ElevenLabs proxy error: {e}")

    frontend_thread = threading.Thread(target=receive_from_frontend, daemon=True)
    frontend_thread.start()

    try:
        asyncio.run(elevenlabs_proxy())
    except (KeyboardInterrupt, ConnectionResetError):
        print("Connection terminated.")