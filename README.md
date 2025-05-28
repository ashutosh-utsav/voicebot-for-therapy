# AI Therapist Web Application

This is a simple, real-time, voice-to-voice web application that serves as an AI Therapist. It uses a custom-built agent from the **ElevenLabs Conversational AI** platform for its voice and intelligence.

The application allows a user to speak into their microphone, sends the audio to the ElevenLabs agent, and plays back the AI's spoken response in real-time, creating a seamless conversational experience.


## How It Works

The application is built with a simple but robust architecture:

1.  **Frontend (HTML / JavaScript):** Captures audio from the user's microphone using the `MediaRecorder` API. It establishes a WebSocket connection to the backend server.
2.  **Backend (Flask / Python):** Acts as a secure WebSocket proxy.
    - It receives audio chunks from the frontend.
    - It relays these audio chunks to the ElevenLabs Conversational AI Agent endpoint over another WebSocket.
    - It receives the audio response from ElevenLabs and relays it back to the frontend.
3.  **Frontend (Audio Playback):** The JavaScript on the frontend receives the raw audio stream from the backend, decodes it using the native Web Audio API, and plays it back, creating a continuous conversation.


## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- An active ElevenLabs account with an API Key and a created Conversational AI Agent.

### 1. Clone the Repository

```bash
git clone git@github.com:ashutosh-utsav/voicebot-for-therapy.git
cd AI_therapist_app 
```

### 2. Create Virtual ENV
```bash
virtualenv .envAI
```

### 3. Activate Virtual ENV
```bash
source .envAI/bin/activate
```

### 4. Install Dependencies
```bash
pip install Flask flask-sock gunicorn websockets python-dotenv
```

### 5. Configure Environment Variables
- Create a file named .env in the root of your project directory.
- Add your ElevenLabs API key to this file:
```bash
ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"
```

### 6. Run the application 
```bash
gunicorn --worker-class gthread --threads 8 --bind 0.0.0.0:5050 app:app
```
