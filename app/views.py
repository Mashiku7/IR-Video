from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for, flash, Response, jsonify
import time
from app.init_app.py import app
import random
import youtube_dl
import urllib.request
import untangle
import re
import sys

import SpeechRecognition as sr

from celery import Celery



celery = Celery(app.import_name, backend='redis://localhost:6379/0',
                broker='redis://localhost:6379/0')

#taskprogress = {}

@celery.task(bind=True)
def process_video(self, url):
    """Background task that runs a long function with progress reports."""
    def progress_cb(done, total):
        self.update_state(state='PROGRESS',
                          meta={'current': done, 'total': total})
    #tag.tag_and_upload(url, progress_cb)
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42}

@app.route("/")
def home_page():
    return render_template('pages/home_page.html')

@app.route("/add")
def add():
    return render_template('pages/add_video.html')

@app.route("/add_video", methods=['POST'])
def add_video(vid):
    url = request.form["url"]
    re1='.*?'	# Non-greedy match on filler
    re2='(?:[a-z][a-z0-9_]*)'	# Uninteresting: var
    re3='.*?'	# Non-greedy match on filler
    re4='(?:[a-z][a-z0-9_]*)'	# Uninteresting: var
    re5='.*?'	# Non-greedy match on filler
    re6='(?:[a-z][a-z0-9_]*)'	# Uninteresting: var
    re7='.*?'	# Non-greedy match on filler
    re8='(?:[a-z][a-z0-9_]*)'	# Uninteresting: var
    re9='.*?'	# Non-greedy match on filler
    re10='(?:[a-z][a-z0-9_]*)'	# Uninteresting: var
    re11='.*?'	# Non-greedy match on filler
    re12='(?:[a-z][a-z0-9_]*)'	# Uninteresting: var
    re13='.*?'	# Non-greedy match on filler
    re14='((?:[a-z][a-z0-9_]*))'	# Variable Name: vid

    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10+re11+re12+re13+re14,re.IGNORECASE|re.DOTALL)
    m = rg.search(url)
    if m:
        vid=m.group(1)
    task = process_video.apply_async(args=[url])
    #taskprogress[task.id] = 0
    youtube_url = 'https://www.youtube.com/watch?v=' + vid
    if True == is_url_ok(youtube_url):
        hed = """<h2><a href="{url}">YouTube video: {id}</a></h2>""".format(url=youtube_url, id=vid)
        iframe = IFRAME_TEMPLATE.substitute(youtube_id=vid)
    else:
        # when the youtube video id is not found
        hed = """<h2>Youtube video {id} <strong>does not exist</strong></h2>""".format(id=vid)
        # note that we substitute a specific YouTube ID for the template
        iframe = IFRAME_TEMPLATE.substitute(youtube_id='sQK3Yr4Sc_k')

    return hed + iframe, jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route("/ask")
def ask(vid, sub):
    #sub=parameter from input question of user

    # Record Audio
    sub = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("You said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


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
    
    xml_captions_url = 'http://video.google.com/timedtext?lang=en&v=' + vid
    
    try:
        obj = untangle.parse(xml_captions_url)
    except Exception:
        print("This video does not contain captions provided by google.")
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
        #Download caption and search for parameter or parameters with start time stamp

    
    
    
    return render_template('pages/ask_video.html')

@app.route("/ask_video", methods=['POST'])
def add_video(vid, ts):
    url = request.form["url"]
    task = process_video.apply_async(args=[url])
    #taskprogress[task.id] = 0
    if True == is_url_ok(youtube_url):
        hed = """<h2><a href="{url}">YouTube video: {id}</a></h2>""".format(url=youtube_url, id=vid)
        iframe = IFRAME_TEMPLATE.substitute(youtube_id=vid)
        iframe = IFRAME_TEMPLATE.substitute(time_stamp=ts)
    else:
        # when the youtube video id is not found
        hed = """<h2>Youtube video {id} <strong>does not exist</strong></h2>""".format(id=vid)
        # note that we substitute a specific YouTube ID for the template
        iframe = IFRAME_TEMPLATE.substitute(youtube_id='sQK3Yr4Sc_k')

    return hed + iframe, jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 100:
            x = x + 10
            time.sleep(0.2)
            yield "data:" + str(x) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')



@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = process_video.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
