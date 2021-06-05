# <snippet_imports>
import os
from dotenv import load_dotenv
load_dotenv()

# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient 
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person ,Error
# </snippet_imports>


ENDPOINT=os.environ.get('ENDPOINT')
KEY=os.environ.get('KEY')

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
