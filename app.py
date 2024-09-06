from flask import Flask, render_template, session
from flask_session import Session
from models import CARDS, db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
with app.app_context():
    db.create_all()

import requests
import json

app.config ['SECRET_KEY'] ="1234"
app.config ['SESSION_TYPE'] ="filesystem"
app.config ['SESSION_FILE_THRESHOLD'] =500
Session(app)

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/new_game')
def get_deck():
	#hand.clear()
	#dealer.clear()
	#result.clear()
	deck_id = json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
	remaining = json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['remaining']
	session['deck_id']=deck_id
	session['remaining']=remaining
	hand = []
	sumhand = 0
	sumdealer = 0
	dealer = []
	
	for j in range(2):
		#игрок берет 2 карты
		card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
		card_image=card['images']['png']
		remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
		if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
			card['value']=10
		elif card['value'] == 'ACE':
			card['value']=11
		else:
			card['value']=card['value']
		hand.insert(0, card)
		sumhand = [i['value'] for i in hand]
		sumhand = sum([int(i) for i in sumhand])
			
		#дилер берет 2 карты
		card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
		card_image=card['images']['png']
		remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
		if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
			card['value']=10
		elif card['value'] == 'ACE':
			card['value']=11
		else:
			card['value']=card['value']
		dealer.insert(0, card)
		sumdealer = [i['value'] for i in dealer]
		sumdealer = sum([int(i) for i in sumdealer])
			
	session['hand'] = hand
	session['dealer'] = dealer
	session['sumhand'] = sumhand
	session['sumdealer'] = sumdealer
	session.modified = True
		
	return render_template('index.html',card_image=card_image,deck_id=deck_id, remaining=remaining, hand=hand, sumhand=sumhand, dealer=dealer, sumdealer=sumdealer)

@app.route('/get_card')
def get_card():
	deck_id = session.get('deck_id')
	remaining = session.get('remaining')
	sumhand = session.get('sumhand')
	sumdealer = session.get('sumdealer')
	hand = session.get('hand')
	dealer = session.get('dealer')

	#игрок берет 1 карту
	#result.clear()
	card=json.loads(requests.get('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)['cards'][0]
	card_image=card['images']['png']
	remaining =json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/').text)['remaining']
	if card['value'] == 'KING' or card['value'] == 'JACK' or card['value'] == 'QUEEN':
		card['value']=10
	elif card['value'] == 'ACE':
		card['value']=11
	else:
		card['value']=card['value']
		
	session['hand'].insert(0, card) #?
	sumhand = [i['value'] for i in hand]
	sumhand = sum([int(i) for i in sumhand])
		
	sumdealer = [i['value'] for i in dealer]
	sumdealer = sum([int(i) for i in sumdealer])
	
	session.modified = True
	
	new_card_to_db = CARDS(deck_id = session.get('deck_id'), datetime = datetime.now(), card = card['code'])#
	db.session.add(new_card_to_db)
	db.session.commit()
	
	return render_template('index.html',card_image=card_image,deck_id=deck_id, remaining=remaining, hand=hand, sumhand=sumhand, dealer=dealer, sumdealer=sumdealer)

@app.route('/game_result')
def game_result():
	sumhand = session.get('sumhand')
	sumdealer = session.get('sumdealer')
	#результат игры
	if sumhand > 21 and sumdealer <= 21:
		print('You loose')
	elif sumhand <= 21 and sumhand > sumdealer:
		print('You win')
	elif sumhand <= 21 and sumdealer > 21:
		print('You win')
	else:
		print('You still not loose')
	
	session.modified = True
	
	return render_template('index.html', sumhand=sumhand, sumdealer=sumdealer)

@app.route('/view_db')
def view_db():
	cards_db = CARDS.query.all()
	return render_template('view_db.html', cards_db=cards_db)

if __name__ == '__main__':
 app.run(debug=True)