import urllib.request
import untangle
import sys

def allindices(string, sub):
    listindex=[]
    i = string.find(sub)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)
    return listindex
def search(query):
    indices = allindices(complete_caption.upper(),query.upper())
    if (len(indices)==0):
        return "Keyword not found"
    else:
        newset = set()
        for index in indices:
            if (index in keyword.keys()):
                newset.add(keyword[index])
            else:
                curr = 0
                for i in list(keyword.keys()):
                    if i < index:
                        curr = i
                newset.add(keyword[curr])
        return "Matching times: "+str(sorted(list(newset)))

#uses google provided captions
orig = input("Please paste the entire url of the youtube video: ")
url = "http://video.google.com/timedtext?lang=en&v="+orig[len("https://www.youtube.com/watch?v="):]


try:
    obj = untangle.parse(url)
except Exception:
    print("This video does not contain captions provided by google.")
    #print("Following service provided by IBM Watson")
    #use ibm watson here
    #import youtube_dl

    #options = {
    #'format': 'bestaudio/best', # choice of quality
    #'extractaudio' : True,      # only keep the audio
    #'audioformat' : "wav",      # convert to mp3
    #'outtmpl': 'rawaudio.wav',        # name the file the ID of the video
    #'noplaylist' : True,        # only download single song, not playlist
    #}
    #with youtube_dl.YoutubeDL(options) as ydl:
    #ydl.download([orig])
    #print("File audio extracted")
    # import json
    # from os.path import join, dirname
    # from watson_developer_cloud import SpeechToTextV1
    # speech_to_text = SpeechToTextV1(
    #     username='9e54b45c-6560-47e3-b798-aff222850fbf',
    #     password='iydT2ZkN3ftT',
    #     x_watson_learning_opt_out=False
    # )
    #
    # print(json.dumps(speech_to_text.models(), indent=2))
    #
    # print(json.dumps(speech_to_text.get_model('en-US_BroadbandModel'), indent=2))
    #
    # with open('rawaudio.wav', 'rb') as audio_file:
    #     print(json.dumps(speech_to_text.recognize(
    #         audio_file, content_type='audio/wav', timestamps=True, word_confidence=True), indent=2))
    #end ibm watson translation
    exit()
obj = obj.transcript.text
complete_caption = ""
keyword = {}
index = 0
for text in obj:
    complete_caption += text.cdata
    for item in text.cdata.split():

        m, s = divmod(float(text['start']), 60)
        h, m = divmod(m, 60)
        keyword[index]= "%d:%02d:%02d" % (h, m, s)
        index += len(item)+1
    index-=1

while True:
    x = input("Find: ")
    if (x=="exit"):
        break
    print(search(x))
