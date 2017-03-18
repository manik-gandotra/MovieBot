import requests
import json
from flask import Flask,request
import apiai
ACCESS_TOKEN="EAASJHfZAHf9MBAN4NWQRVl4nTElGppxeYMY9XnNyXficZCpl2SpZBBsqJpC3rMdPDDfOjQ613cvS0jPNyDYQstAFlchxK8pjngQ4Y5uoRSQxA3kMHuhg48dtnvgWOTmaxWck3JIZCMS7qy9zrSFDu6qT0sRrSzglhzBBSnlkJgZDZD"
CLIENT_ACCESS_TOKEN="476fa6821c5c4aa0ac144e0bdbbac9e1"
ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
app=Flask(__name__)
@app.route("/",methods=['GET'])
def verify():
	# our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return 'Hello World (from Flask!)', 200

def reply(user_id, msg,genre):
    
    fbmess=""
    if genre != NULL:
        if genre=="comedy":
            fbmess="21 JUMP STREET, Forrest Gump, Ted."
        elif genre=="romantic":
            fbmess="Crazy stupid love, About Time, Titanic."
        elif genre=="drama":
            fbmess="Dead poet's society, Good will hunting, Lion."
        elif genre=="thriller":
            fbmess="Shutter island, Inception, Gone girl."
        elif genre=="horror":
            fbmess="The ring, Final destination series, Wrong turn series."
    
    if fbmess=="":     
        data = {
            "recipient": {"id": user_id},
            "message": {"text": msg}
        }
    else:
        data={
            "recipient": {"id": user_id},
            "message": {"text": msg},
            "facebook":{fbmess}
        }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']

    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = message

    # get response from API.ai
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    if 'result' in response_obj:
        response = response_obj["result"]["fulfillment"]["speech"]
        genre=response_obj["result"]["contexts"][0]["parameters"]["genre.original"]
    reply(sender, response,genre)
    reply(sender,response)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)