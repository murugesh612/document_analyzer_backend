from flask_socketio import SocketIO
from injector import inject
from services.transcribe_summary_service import TranscribeSummary
from websockets_resources.websocket_resource import WebSocketResource
from services.logger import Logger


class WebSocketAudioResource(WebSocketResource):
    """Class to handle the audio processing using web sockets"""

    audio_chunks = []

    @inject
    def __init__(
        self,
        socketIO: SocketIO,
        transcribe_service: TranscribeSummary,
        logger: Logger,
    ):
        self.socketIO = socketIO
        self.transcribe_service = transcribe_service
        self.logger = logger

        self.socketIO.on_event(
            "audio_chunk",
            namespace=self.signalling_server_namespace,
            handler=self.__handle_audio_track_event__,
        )
        self.logger.info('WebSocketAudioResource service is running')

    def __handle_audio_track_event__(self, data):
        """Method to handle the audio track event"""

        print("handle audio event hit")

        caller_id = data["callerId"]

        if not caller_id:
            raise Exception("Caller Id not found")

        audio_data = data["base64AudioChunk"]
        if not audio_data:
            raise Exception("Audio data not found")
