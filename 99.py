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
pregame_numbers = {}
i2c = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
c2i = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13}

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    body = request.values.get('Body', None)
    send_num = request.values.get('From', None)
    
    message = ''
    
    if body[:5] == 'admin':
        all_message = body[6:]
        current_players = active_numbers[send_num].players
        for p in current_players:
            send_message(p.number, '[SERVER_MESSAGE]' + all_message)
    elif send_num in pregame_numbers:
        #print(pregame_numbers)
        if pregame_numbers[send_num] == 0:
            first_player = Player(body, send_num)
            active_numbers[send_num].new_player(first_player)
            message = "Nice to meet you " + body + '. Now please text me the names of the players you would like to add to the game in this format \'Name: Phone Number\''
            pregame_numbers[send_num] = 1
        elif pregame_numbers[send_num] == 1:
            if body == 'Done':
                pregame_numbers.pop(send_num)
                current_game = active_numbers[send_num]
                current_game.start_game()
                #Sketchy method to make Jay go first
                if len(current_game.players) > 1:
                    player_temp = current_game.players.pop(0)
                    current_game.players.insert(1, player_temp)
                player_one = current_game.players[0]
                for p in current_game.players:
                    cards = p.cards
                    cards = [i2c[i-1] for i in cards]
                    start_message = "[TEST_BUILD] Hello! You've been invited to play 99! You're cards are "
                    start_message += str(cards)
                    start_message += ". " + player_one.name + " is up first!"
                    send_message(p.number, start_message)
                for p in current_game.players:
                    quick_note = 'If you are trying to play a 10 or A, specify your action by adding a + or - (e.g. A- specifies 1)'
                    send_message(p.number, quick_note)
            else:
                new_name, new_num = body.split(": ")
                if (new_num[0] != '+') | (len(new_num) != 12):
                    message = 'Number was not in required format! Needs to be \'+1**********\''
                else:
                    current_game = active_numbers[send_num]
                    new_player = Player(new_name, new_num)
                    current_game.new_player(new_player)
                    active_numbers[new_num] = current_game
                    message = 'Great! ' + new_name + ' was added to your game. Text \'Done\' when all players have been added.'
    elif send_num in active_numbers:
        if not active_numbers[send_num].started:
            message = "Oops! Looks like you are in a game that hasn't yet started, hold tight!"
        else:
            current_game = active_numbers[send_num]
            current_player = current_game.next_player()
            if current_player.number != send_num:
                message = 'It\'s not your turn yet! Please wait for ' + current_player.name + '.'
            else:
                player_cards = current_player.cards
                player_cards = [i2c[i-1] for i in player_cards]
                choice = ''
                if (body == 'A+') | (body == '10+') | (body == 'A-') | (body == '10-'):
                    choice = body[len(body) - 1:]
                    body = body[:len(body) - 1]
                if not body in player_cards:
                    message = 'That\'s not a valid move! Your cards are ' + str(player_cards) + '.'
                else:
                    [stack, reversed, game_over] = current_game.play(c2i[body], choice)
                    if game_over:
                        over_message = current_player.name + ' has played a ' + body
                        over_message += '. This pushed the stack over 99. ' + current_player.name + ' loses!'
                        for p in current_game.players:
                            active_numbers.pop(p.number)
                    else:
                        for p in current_game.players:
                            play_message = current_player.name + ' has played a ' + body
                            play_message += '. The stack value is now ' + str(stack)
                            if reversed:
                                play_message += '. The order was reversed'
                            play_message += '. Your current cards are ' + str([i2c[i-1] for i in p.cards])
                            play_message += '. It is now ' + current_game.next_player().name + '\'s turn!'
                            send_message(p.number, play_message)
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
    
