import datetime
import base64
import requests
import json
from twilio.rest import Client
import app

class Actions:

    resetInterval = 60   # Reset Interval is 1min
    
    # These below block are static variables

    offlineUrl = 'http://192.168.139.181:5000'

    sentTime = None
    resetTime = None
    client = None

    threatLabel = None
    
    def __init__(self):
        self.resetTime = datetime.datetime.now()
        self.client = Client(Actions.account_sid, Actions.auth_token)
        
    def NotifyOwner(self,label):
        
        if datetime.datetime.now() >= self.resetTime:    
            print("Sending Notification Now")
            self.threatLabel = label

            try:
                with open('static/currentDetection.jpg','rb') as img:
                    image = base64.b64encode(img.read())
            
                sentAt = Actions.url+'?key='+Actions.api_key
                
                try:
                    req = requests.post(sentAt, data={'image':image})
                    response = req.text

                    resParse = json.loads(response)
                    imageUrl = resParse['data']['display_url']
                    
                    try:
                        message = self.client.messages.create(
                            from_='whatsapp:+14155238886',
                            body=f'Hello Master!! I Have Detected suspecious activity at home.\nFound: {self.threatLabel}\nRealTime Image: {imageUrl}\nTake Actions at: {self.offlineUrl}',
                            to='whatsapp:+918275934108'
                        )

                        print('Current Message Status:',message.status)

                    except:
                        print('Error Sending Whatsapp Notification')    
                except:
                    print("Error Uploading image")
                    print("Initiating the Offline Measures!!")
                    app.InitLockdown()
                    
            except:
                print("Error Opening current file")

            self.sentTime = datetime.datetime.now().time()
            self.resetTime = datetime.datetime.now() + datetime.timedelta(seconds=self.resetInterval)

        else:
            print("No Need To send the notification!! Already Notified")

