from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)
account_sid = 'ACa77cec72b91ee091ea25a32b97374eaa'
auth_token = '6697edbf300df7cad71886684643b593'
client = Client(account_sid, auth_token)
active_numbers = {}
games = []

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    body = request.values.get('Body', None)
    send_num = request.values.get('From', None)
    
    message = ''
    
    if send_num in active_numbers:
        message = 'In development'
    elif body == 'Create Game':
        new_game = Game()
        active_numbers[send_num] = new_game
        message = 'You have started a game! Please text me the names of the players you would like to add in this format \'Name: Phone Number\''
    else:
        message = 'Welcome to 99! You don\'t seem to be in a game right now, text me \'Create Game\' to get started!'
    
    resp = MessagingResponse()

    #message = send_num + ": " + body
    resp.message(message)

    return str(resp)

def send_message(recieve_num, message):
    message = client.messages \
    .create(
         body=message,
         from_='+15623837899',
         to=recieve_num)
    
if __name__ == "__main__":
    app.run(debug=True)
    