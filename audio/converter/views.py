from django.shortcuts import render
import pyttsx3
import os
from django.core.files.storage import FileSystemStorage
import mimetypes
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Create your views here.
def home(request):
    return render(request,'converter/home.html')
def voicetotext(request):
    if request.method=='POST':
        files=request.FILES['Document']
        fs = FileSystemStorage()
        fs.save(files.name,files)
        doc_file=files.name
        tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        file_name='media/'+doc_file
        print(file_name)
        input_audio, _ = librosa.load(file_name, 
                                sr=16000)
        input_values = tokenizer(input_audio, return_tensors="pt").input_values
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.batch_decode(predicted_ids)[0]
        f = open("audiototextfile.txt", "w")
        f.write(transcription)
        f.close()
        return render(request,'converter/voicetotext.html',{"data":transcription})
    return render(request,'converter/voicetotext.html')
def texttovoice(request):
    if request.method=='POST':
        text=request.POST['text']
        obj=pyttsx3.init()
        obj.say(text)
        obj.save_to_file(text, 'files/speech.mp3')
        obj.runAndWait()
    return render(request,'converter/texttovoice.html')
def download(request):
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename='speech.mp3'
    filepath=base_dir+'\\files\\'+filename
    thefile=filepath 
    filename=os.path.basename(thefile)
    chunk_size=8192
    response=StreamingHttpResponse(FileWrapper(open(thefile,'rb'),chunk_size),content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length']=os.path.getsize(thefile)
    response['Content-Disposition']="Attachment;filename=%s" % filename
    return response
def download1(request):
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename='audiototextfile.txt'
    filepath=base_dir+'\\'+filename
    thefile=filepath 
    filename=os.path.basename(thefile)
    chunk_size=8192
    response=StreamingHttpResponse(FileWrapper(open(thefile,'rb'),chunk_size),content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length']=os.path.getsize(thefile)
    response['Content-Disposition']="Attachment;filename=%s" % filename
    return response
