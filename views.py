from flask import Flask,request
import traceback
import json
from  models import dbSetUp

app=Flask(__name__)
token = "<ACCESS_TOKEN_HERE>"

dbSetUp()


@app.route('/webhook',methods=['GET','POST'])
def webhook():
    if request.method=='POST':
        try:
            data=json.loads(request.data)
            text=data['entry'][0]['messaging'][0]['message']['text']
            sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
            payload = {'recipient': {'id': sender}, 'message': {'text': "Hello World"}} # We're going to send this back
            r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
        except Exception as e:
            print( traceback.format_exc()) # something went wrong
    elif request.method == 'GET': # For the initial verification

        if request.args.get('hub.verify_token') == '<VERIFY_TOKEN_HERE>':
           return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Hello World" #Not Really Necessary






#check a user exists. Return True or false

def check_user(sender_id):
    connection=r.connect('localhost',28015)
    count=r.db('remember_bot').table('user').filter({'user_id':sender_id}).count().run(connection)
    if count>0:
        #user exists
        user=r.db('remember_bot').table('user').filter({'user_id':sender_id}).run(connection)
        connection.close()
        return True
    
    connection.close()
    return False



#saves a key value pair in post table for each user in following format
'''  {
        "key":key,
        "value":value,
        "sender_id":sender_id,
        "time":time_object

    }
'''

def save_post(sender_id,key,value):
    connection=r.connect('localhost',28015)
    #insert key value to table post
    res=r.db('remember_bot').table('post').insert({"key":key,"value":value,"sender_id":sender_id,"time":r.now()}).run(connection)
    connection.close()
    return res





    
    
