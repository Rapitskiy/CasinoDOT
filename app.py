from flask import Flask, render_template
app = Flask(__name__)

import requests
import json
global deck
global remaining
global dealer
global result
sumhand = 0
sumdealer = 0
hand = []
dealer = []
result = []

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/new_game')
def get_deck():
	hand.clear()
	dealer.clear()
	result.clear()
	deck =json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
	remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['remaining']
	return render_template('index.html',deck=deck, remaining=remaining)

@app.route('/get_card/<deck_id>')
def get_card(deck_id):
	if hand == []:
		card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
		card_image=card['images']['png']
		remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
		if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
			card['value']=10
		elif card['value'] == 'ACE':
			card['value']=11
		else:
			card['value']=card['value']
		hand.append(card)
		sumhand = [i['value'] for i in hand]
		sumhand = sum([int(i) for i in sumhand])
		card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
		card_image=card['images']['png']
		remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
		if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
			card['value']=10
		elif card['value'] == 'ACE':
			card['value']=11
		else:
			card['value']=card['value']
		dealer.append(card)
		sumdealer = [i['value'] for i in dealer]
		sumdealer = sum([int(i) for i in sumdealer])
		#2раз
		card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
		card_image=card['images']['png']
		remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
		if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
			card['value']=10
		elif card['value'] == 'ACE':
			card['value']=11
		else:
			card['value']=card['value']
		hand.append(card)
		sumhand = [i['value'] for i in hand]
		sumhand = sum([int(i) for i in sumhand])
		card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
		card_image=card['images']['png']
		remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
		if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
			card['value']=10
		elif card['value'] == 'ACE':
			card['value']=11
		else:
			card['value']=card['value']
		dealer.append(card)
		sumdealer = [i['value'] for i in dealer]
		sumdealer = sum([int(i) for i in sumdealer])
	else:
		card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
		card_image=card['images']['png']
		remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
		if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
			card['value']=10
		elif card['value'] == 'ACE':
			card['value']=11
		else:
			card['value']=card['value']
		hand.append(card)
		sumhand = [i['value'] for i in hand]
		sumhand = sum([int(i) for i in sumhand])
		sumdealer = [i['value'] for i in dealer]
		sumdealer = sum([int(i) for i in sumdealer])
	if sumhand > 21:
		result.append("You loose")
	else:
		result.append("You still not loose")
	return render_template('index.html',card_image=card_image,deck=deck_id, remaining=remaining, hand=hand, sumhand=sumhand, dealer=dealer, sumdealer=sumdealer, result=result)

#@app.route('/get_card/<deck_id>')
#def game_result(deck_id):
	
if __name__ == '__main__':
 app.run(debug=True)