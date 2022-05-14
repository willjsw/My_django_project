from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

topics = [
    {"id":1, "title":"routing", "body":"routing is.."},
    {"id":2, "title":"view", "body":"view is.."},
    {"id":3, "title":"Model", "body":"Model is.."},
]

nextId = 4

def HTMLTemplate(article,id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
        <li>
            <form action="/delete/" method="post">
                <input type="hidden" name="id" value={id}>
                <input type="submit" value="delete">
            </form>
        </li>
        <li><a href="/update/{id}">update</a></li>
        '''
    ol = ""
    for topic in topics:
        ol +=f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ol>
            {ol}
        </ol>
        {article}
        <li>
            <a href="create">Create</a>
        </li>
        {contextUI}
    </body>
    </html>
    '''

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello Django
    '''
    return HttpResponse(HTMLTemplate(article))


def read(request, id):
    global topics
    article = ""
    for topic in topics:
        if topic["id"] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article,id))

@csrf_exempt
def create(request):
    global nextId
    if request.method == "GET":
        article = '''
            <form action="/create/" method="POST">
                <p><input type="text" placeholder="title" name="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    else:
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)
        nextId +=1
        return redirect(url)

@csrf_exempt
def delete(request):
    global topics
    if request.method == "POST":
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic["id"] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')

@csrf_exempt
def update(request,id):
    global topics
    if request.method == "GET":
        for topic in topics:
            if topic["id"] == int(id):
                selectedTopic = {
                    "title":topic["title"],
                    "body":topic["body"],
                }
        article = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" placeholder="title" name="title" value={selectedTopic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic["body"]}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article,id))
    else:
        title = request.POST["title"]
        body = request.POST["body"]
        for topic in topics:
            if topic["id"] == int(id):
                topic["title"] = title
                topic["body"] = body
        return redirect(f'/read/{id}')