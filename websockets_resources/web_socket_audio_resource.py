from flask_socketio import SocketIO
from injector import inject
from websockets_resources.websocket_resource import WebSocketResource
from services.logger import Logger


class WebSocketAudioResource(WebSocketResource):
    """Class to handle the audio processing using web sockets"""

    @inject
    def __init__(
        self,
        socketIO: SocketIO,
        logger: Logger,
    ):
        self.socketIO = socketIO
        self.logger = logger

        self.socketIO.on_event(
            "audio_chunk",
            namespace=self.signalling_server_namespace,
            handler=self.__handle_audio_track_event__,
        )
        self.logger.info('WebSocketAudioResource service is running')

    def __handle_audio_track_event__(self, data):
        """Method to handle the audio track event"""

        caller_id = data["callerId"]

        if not caller_id:
            raise Exception("Caller Id not found")

        print("data")
        print(caller_id)

        audio_data = data["audioChunk"]
        if not audio_data:
            raise Exception("Audio data not found")

        binary_data = "".join(format(byte, "08b") for byte in audio_data)  # noqa
        # byte_chunks = [
        #     binary_data[i: i + 8] for i in range(0, len(binary_data), 8)
        # ]  # noqa

        # # Step 2: Convert each binary chunk to an integer (byte)
        # byte_array = bytearray(int(chunk, 2) for chunk in byte_chunks)

        # # Step 3: Decode the byte array into a string (assumes UTF-8 encoding)
        # decoded_string = byte_array.decode("utf-8", errors="ignore")

        print("audio chunk event hit")
        print(binary_data)

        print("type of data")
        print(type(binary_data))
