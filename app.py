from dotenv import load_dotenv
from flask_cors import CORS

from flask_app import app
from flask_smorest import Api

from resources.twilio_resource import twilio_blueprint
from resources.transcribe import bp as transcribe_bp
from resources.phone_call_resource import phone_call_blueprint
from resources.documents_resource import documents_blueprint
from services.logger import Logger
from utils.app_config import (
    get_app_config,
    get_injector_instance,
)
from services.vectorstore_service import VectorStoreService
from websockets_resources.web_rtc_signalling_server import (
    WebRTCSignallingServer,
)
from websockets_resources.web_socket_audio_resource import (
    WebSocketAudioResource,
)

# loading .env file
load_dotenv()

# adding CORS
CORS(app)

# database initialization
database_service = VectorStoreService()

# getting app config
config = get_app_config(app, database_service)

logger = get_injector_instance().get(Logger)

# Registering the api endpoint resources
api = Api(app)
api.register_blueprint(twilio_blueprint)
api.register_blueprint(transcribe_bp)
api.register_blueprint(phone_call_blueprint)
api.register_blueprint(documents_blueprint)


# Registering the web sockets
web_socket_server = get_injector_instance().get(WebRTCSignallingServer)
web_socket_audio_resource = get_injector_instance().get(WebSocketAudioResource)
