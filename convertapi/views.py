from rest_framework import generics, status, views, permissions
from .serializers import UploadSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from drf_yasg import openapi
from django.http import HttpResponsePermanentRedirect
import tempfile
from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import default_storage
import time
import csv
from django.core.files.base import ContentFile
import uuid
import zipfile
from django.http import FileResponse
from io import StringIO
from PyPDF2 import PdfFileReader
import shutil
from io import BytesIO
import threading
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from authentication.models import  User
from .models import Convert
from rest_framework import viewsets
from .serializers import ConvertSerializerLoc
# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path,file_name):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=100,
    )

    
    folder_name = "audio-chunks"
    fh = open(file_name+".txt", "w+") 
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.listen(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                # text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                fh.write(text+". ") 
                whole_text += text
    # return the text for all chunks detected



    print(User.objects.all())
    return whole_text

class FileUploadView(views.APIView):
    serializer_class = UploadSerializer
    file_path = ''
    file_name = ''
    path = ''
    user_id = None
    convert_id = None
    def run(self):
        command = "ffmpeg -i "+self.path+self.file_name+".mp4 "+self.path+self.file_name+".mp3"
        os.system(command)

        commandwav = "ffmpeg -i "+self.path+self.file_name+".mp3 "+self.path+self.file_name+".wav"
        os.system(commandwav)

        print(get_large_audio_transcription(self.path+self.file_name+".wav",self.path+self.file_name))
        Convert.objects.filter(pk=self.convert_id).update(status='completed')

    def post(self,request,user_id,format=None):
        self.user_id = user_id
        data = request.data['file']
        print(data._name)
        # return Response(status=200)

        if data.content_type != 'video/mp4':
            return Response(status=400)
        unique_filename = str(uuid.uuid4())
        self.path = 'convert/'+str(self.user_id)+ '/'
        self.file_name = unique_filename
        self.file_path =  self.path +self.file_name+'.mp4'
        text_file_name = self.path +self.file_name+'.txt'
        print(self.path,self.file_name)
        convert = Convert.objects.create(file_name=data._name,path=text_file_name,status='start',user_id = self.user_id )
        self.convert_id = convert.pk
        path = default_storage.save(str(self.user_id)+ '/'+self.file_name+'.mp4', ContentFile(data.read()))
        print(path,'----------')
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                           
        thread.start()   

        return Response(status=200)




class ConvertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Convert.objects.all()
    serializer_class = ConvertSerializerLoc
