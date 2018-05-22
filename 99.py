from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from Game import Game, Cards
from Player import Player

app = Flask(__name__)
account_sid = 'ACa77cec72b91ee091ea25a32b97374eaa'
auth_token = '6697edbf300df7cad71886684643b593'
client = Client(account_sid, auth_token)
active_numbers = {}
games = []
pregame_numbers = {}

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    body = request.values.get('Body', None)
    send_num = request.values.get('From', None)
    
    message = ''
    if send_num in list(pregame_numbers.keys):
        if pregame_numbers[send_num] == 0:
            active_numbers[send_num].new_player(body, send_num)
            message = "Nice to meet you " + body + '. Now please text me the names of the players you would like to add to the game in this format \'Name: Phone Number\''
            pregame_numbers[send_num] = 1
        if pregame_numbers[send_num] == 1:
            if body == 'Done':
                pregame_numbers.pop(send_num)
                active_numbers[send_num].start_game()
            new_name, new_num = body.split(": ")
            if new_num[0] != '+' | len(new_num) != 12:
                message = 'Number was not in required format! Needs to be \'+1**********\''
            else:
                current_game = active_numbers[send_num]
                current_game.new_player(new_name, new_num)
                active_numbers[new_num] = current_game
                message = 'Great! ' + new_name + ' was added to your game. Text \'Done\' when all players have been added.'
    elif send_num in list(active_numbers.keys):
        if not active_numbers[send_num].started:
            message = "Oops! Looks like you are in a game that hasn't yet started, hold tight!"
        else:
            message = "In Development, Game started!"
    elif body == 'Create Game':
        new_game = Game()
        active_numbers[send_num] = new_game
        pregame_numbers[send_num] = 0
        message = 'You have started a game! First, let me know what your name is!'
    else:
        message = 'Welcome to 99! You don\'t seem to be in a game right now, text me \'Create Game\' to get started!'
    
    resp = MessagingResponse()
    if message != '':
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
    