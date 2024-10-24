import os
import json
import threading
import websocket

ASSEMBLYAI_WEBSOCKET_URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000" # noqa
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")


class AssemblyAIWebSocketService:
    """Service to handle communication with AssemblyAI WebSocket API"""

    def __init__(self):
        self.ws = None
        self.is_connected = False
        self.thread = None

    def connect(self):
        """Start the AssemblyAI WebSocket connection in a separate thread"""
        self.thread = threading.Thread(target=self.__connect_to_assemblyai__)
        self.thread.start()

    def __connect_to_assemblyai__(self):
        """Connect to AssemblyAI's real-time WebSocket API"""
        self.ws = websocket.WebSocketApp(
            ASSEMBLYAI_WEBSOCKET_URL,
            header={"Authorization": ASSEMBLYAI_API_KEY},
            on_message=self.__on_transcription__,
            on_error=self.__on_error__,
            on_close=self.__on_close__,
        )
        self.ws.on_open = self.__on_open__
        self.ws.run_forever()

    def __on_open__(self, ws):
        """Callback when WebSocket connection is opened"""
        self.is_connected = True
        print("Connected to AssemblyAI WebSocket")

    def __on_transcription__(self, ws, message):
        """Handle transcription result from AssemblyAI"""
        response = json.loads(message)
        if "text" in response:
            transcription = response["text"]
            print(f"Transcription: {transcription}")
            # TODO: send back the trancription to frontend after summarizing

    def __on_error__(self, ws, error):
        """Handle WebSocket errors"""
        print(f"AssemblyAI WebSocket error: {error}")

    def __on_close__(self, ws, close_status_code, close_msg):
        """Callback when WebSocket connection is closed"""
        self.is_connected = False
        print(f"Connection to AssemblyAI WebSocket closed: {close_status_code}, {close_msg}") # noqa

    def send_audio(self, audio_bytes):
        """Send audio data to AssemblyAI WebSocket for transcription"""
        if self.is_connected:
            try:
                self.ws.send(audio_bytes, opcode=websocket.ABNF.OPCODE_BINARY)
                print("Sent audio chunk to AssemblyAI")
            except Exception as e:
                print(f"Error sending audio chunk: {e}")

    def cleanup(self):
        """Close the WebSocket connection"""
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()
        print("AssemblyAI connection closed")
