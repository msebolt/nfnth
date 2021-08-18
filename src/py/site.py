#!/usr/bin/env python
import os, socket, json, types, shutil#, six
from datetime import datetime

DATA = "/mnt/data" #os.pardir
PATH = "/root/nfnth" #os.path.abspath(os.path.dirname(__file__))
REL = os.getcwd()

key_file = open('key.json', mode='r') #include object map...?
key_template = key_file.read()
key_file.close()

def json2obj(data): return json.loads(data, object_hook=lambda d: types.SimpleNamespace(**d))
def obj2json(data): return json.dumps(data.__dict__, indent=4, sort_keys=True, default=lambda o: o.__dict__)

# public
async def index(request):
    return web.FileResponse(PATH + '/src/index.htm')

async def user(request):
    action = request.match_info.get('action', 'salt') #sign validate
    if action == "salt":
        #set secure cookie with salt 1, send salt 2 datetime...
    elif action == "sign":
	#take signature, compare with generated

async def domain(request):
    domain = request.match_info.get('domain', 'arikara.us')
    action = request.match_info.get('action', 'dir') #search private
	
    if action == "private":
	#check signature
	startpath = DATA + '/domain/' + domain + '/private'
    else:
	startpath = DATA + '/domain/' + domain + '/public'

    if action == "search":
        terms = "term="

    for root, dirs, files in os.walk(startpath):
        for f in files:
            path = os.path.join(root, f)
            if not '.' in path:
                search = open(path, "r")
                searchlines = search.readlines()
                search.close()
                for i, line in enumerate(searchlines):
                    if term in line:
                        terms = terms + path + " at " + str(i) + "|"
            else:
                folder = folder + path
                if not term == "root":
                    search = open(path, "r")
                    searchlines = search.readlines()
                    search.close()
                    for i, line in enumerate(searchlines):
                        if term in line:
                            terms = terms + path + " at " + str(i) + "|"
                else:
                    terms = terms + folder + " at |"
    return terms

async def data(request): #track views?
    action = request.match_info.get('action', 'view') #view, edit, delete
    domain = request.match_info.get('domain', 'arikara.us')
    artifact = request.match_info.get('artifact', 'profile') #profile, file

    if action == 'view':
        return web.FileResponse(DATA + '/' + domain + '/' + artifact)
    elif action == 'edit':
        user = await request.post()
        user_data = json2obj(user["data"])
    #elif action == 'delete':
     #   return web.FileResponse(DATA + group + name + '/profile')
    
    return web.Response(text=str("my_callback({['some string 1', '" + name + "', 'whatever data']});"), content_type='text/json')

#async def stream(request):
    #check feed's page source contains {"text":" watching"}...
    #if not, check rss, https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>&orderby=published
    #...for latest feed
#    return web.FileResponse(PATH + '/ur.js') #make "artifact" specific



# server
import asyncio, aiohttp
from aiohttp import web
from concurrent.futures import ProcessPoolExecutor

def run(part, *args):
    loop = asyncio.new_event_loop()

    try:
        full = part(*args)
        asyncio.set_event_loop(loop)
        loop.create_task(full)
        loop.run_forever()
    finally:
        loop.close()

async def site(port):
    app = web.Application(client_max_size=10000000)

    app.router.add_static('/src', '/root/nfnth/src')
    #app.add_routes([web.post('/cash', bank)])
    #app.add_routes([web.get('/jsonp', jsonp)])
    app.add_routes([web.get('/', index)])
    
    runner = web.AppRunner(app)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    await runner.setup()

    site = web.TCPSite(runner, 'localhost', 5000+port)
    await site.start()

try:
    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor(max_workers=14)
    loop.run_in_executor(executor, run, site, 1) #from haproxy
    #loop.run_in_executor(executor, run, mail, 2)

    loop.run_forever()
except:
    pass
#finally:
#    for runner in runners:
#        loop.run_until_complete(runner.cleanup())

#https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv
#depth/object detection		

#async def user(request):
#    name = request.match_info.get('name', 'matt')
#    action = request.match_info.get('action', 'check')

#    if action == "check":
#        return web.Response(text=str(os.path.exists(DATA + name)), content_type='text/html')
#    elif action == "create":
#        data = await request.post()
#        user_client = json2obj(data["user"])
#        path = DATA + user_client["name"]
        #if not os.path.exists(path):
        #    shutil.copy('res/template', path)
        #    key_copy = json2obj(key_template)
        #    key_copy.name = user_client["name"]
         #   key_copy.mail = user_client["mail"]
         #   key_copy.secret = user_client["secret"]
            #send mail...
         #   with open(path + '/key.json', 'wb') as f:
         #       f.write(obj2json(key_copy))
         #   return web.Response(text=obj2json(await scrub(key_copy)), content_type='text/html')
       # user_file = open(USER_DATA + name + '/key.json', mode='r') #include object map...?
#    user_template = key_file.read()
    #user_file.close()

 #   return json2obj(user_template)

#async def data(request):
 #   async def doc(request): 
 #   name = request.match_info.get('name', 'matt')
 #   doc = request.match_info.get('doc', 'profile')
 #   item = request.match_info.get('item', '') #file

  #  if item == '':
  #      return web.FileResponse(DATA + name + '/doc/' + doc + '/md')
    #else:
    #    return web.FileResponse(USER_DATA + name + '/doc/' + doc + '/item/' + item)
    
   # data = await request.post() #request.json()
   # user_client = json2obj(data["user"])
   # user_server = key(user_client["name"])

#    token = user_client["token"] #add mail support, ip log?
 #   valid = False
 #   if token == user_server.token and not user_server.token == "": #check expires...
  #      valid = True
  #  else:
   #     if user_client["secret"] == user_server.secret: #key? 2fa?
    #        valid = True
     #       user_server.token = "new"

   # if valid is True:
   #     action = user_client["action"]
    #    if action == "reset":
#            user_server.token = ""
 #           with open(USER_DATA + user_client["name"] + '/key.json', 'wb') as f:
  #              f.write(obj2json(user_server))
   #     elif action == "update":
    #        user_client["private"] = user_server.private
     #       with open(USER_DATA + user_client["name"] + '/key.json', 'wb') as f:
      #          f.write(obj2json(user_client))
    #    elif action == "search": #add general search term, receipt...
     #       return await archive(user_client["name"], "general", "")
     #   elif action == "publish":
      #      level = user_client["level"] #md item
       #     sub = user_client["sub"] #new edit delete
        #    doc = user_client["doc"]
         #   path = USER_DATA + name + '/doc/' + doc
          #  if user_client["private"] == "yes":
           #     private = "x"
         #   else:
          #      private = ""
          #  if level == "md": 
           #     if sub == "new":
            #        if not os.path.exists(path):
             #           os.mkdir(path)
       #             with open(path + '/md' + private, 'wb') as f:
        #                f.write(data["doc"])
          #          filename = data['upload'].filename
          #          input_file = data['upload'].file
           #         content = input_file.read() #check file sizes?
         #           with open(os.path.join(path + '/item' + private, filename), 'wb') as f:
         #               f.write(content)
        #        elif sub == "edit":
        #            with open(path + '/md' + private, 'wb') as f:
        #                f.write(data["doc"])
       #         elif action == "delete":
      #              shutil.rmtree(path)
     #       elif level == "item":
   #             item = user_client["item"]
     #           if sub == "new":
  #                 filename = data['upload'].filename
  #                  input_file = data['upload'].file
           #         content = input_file.read() #check file sizes?
          #          with open(os.path.join(path + '/item' + private, filename), 'wb') as f:
         #               f.write(content)
        #        elif sub == "edit":
       #             filename = data['upload'].filename
      #              input_file = data['upload'].file
     #               content = input_file.read() #check file sizes?
    #                with open(os.path.join(path + '/item' + private, filename), 'wb') as f:
   #                     f.write(content)
  #              elif sub == "delete":
 #                   shutil.rmtree(path)
#
     #   return web.Response(text=obj2josn(await(scrub(user_server)), content_type='text/html'))
	
#	import stripe
#stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

#async def bank(request):
    #data = json.loads(await request.json())
 #   intent = stripe.PaymentIntent.create(amount=1499, currency='usd')
 #   secret = intent['client_secret']
#    return web.Response(text='{"clientSecret":"'+secret+'"}')

    #elif action == "pay": #datetime.now().strftime("%d/%m/%Y %H:%M:%S")
     #       transaction = "random" #generate uuid
      #      with open(RECEIPT_DATA + user_client["name"] + transaction, 'wb') as f:
       #         f.write(obj2json(user_client))

#import glob, re#, whois
#from random import randrange

#word_path = '/mnt/res/dictionary.txt'
#with open (word_path, 'r') as f:
#    content = f.read()

#words = re.findall("(\n[A-Z]+[0-9 -]*\n)",content)
#defs = re.findall("\n[A-Z]+[0-9 -]*\n([\s\S]*?)(?=(\n[A-Z]+[0-9 -]*\n))",content)
#NUM_WORDS = 116623 #len(defs) print (len(words)) print (len(defs))
#english = dict()

#i = 0
#while i < len(defs)-1:
#    if not words[i].replace('\n', '') in english:
#        english[words[i].replace('\n', '')] = defs[i][0] #remove dash?
#    else:
#        english[words[i].replace('\n', '')] = english[words[i].replace('\n', '')] + defs[i][0] 
#    i += 1

