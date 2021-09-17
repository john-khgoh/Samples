#!/usr/bin/env python
"""
Blackjack_sim.py: A simple blackjack simulator where the drawn cards are not returned to the deck.
__author__      = "John K H Goh"
__license__ 	= "GPL"
__version__ 	= "0.1.0"
"""
import itertools
from random import shuffle

class Exception(Exception):
	def __init__(self):
		Exception.__init__(self,message, status='error')
		self.message = message
		self.status = status
	def __str__(self):
		return repr(self.value)

class Deck:
	
	def __init__(self,games,players):
		self.suit = self.calc_no_of_suits_required(games,players)
		self.face = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
		self.deck = list(itertools.product(self.face,self.suit))
		self.no_of_players = players
	
	def calc_no_of_suits_required(self,games,players):
		
		max_cards_per_game =  players * 5.5
		rounded_deck_count = max(round((max_cards_per_game/52) * games),1)
		print("%d decks are used in this game. Drawn cards are not returned to the deck.\n" %rounded_deck_count)
		
		suit = []
		for _ in range(rounded_deck_count):
			suit.append("Clubs")
			suit.append("Diamonds")
			suit.append("Hearts")
			suit.append("Spades")
			
		return suit
	
	def shuffle(self): #Shuffling the deck
		shuffle(self.deck)
		
	def draw(self): 
		deck = self.deck[:1]
		del(self.deck[:1]) #Assuming used cards are not returned to the deck
		return deck
	
	def __get_deck__(self):
		return self.deck
		
	def __get_remaining_cards_count__(self):
		return len(self.deck)
		
	def __print_deck__(self):
		for _ in range(len(self.deck)):
			print(self.deck[_])

class Hand:
	
	def __init__(self):
		self.hand = []
		
	def add_hand(self,card):
		self.hand.append(card)
		
	def clear_hand(self):
		self.hand = []
		
	def get_hand(self):
		return self.hand
		
	def get_count(self):
		return len(self.hand)
		
class Blackjack:
			
	def __init__(self,players=4,games=10,player_threshold=17,dealer_threshold=18): 
	#By default, 10 games will be played between 4 players including you and the dealer
		
		self.no_of_players = players #Total number of players including dealer
		self.no_of_other_players = (self.no_of_players - 1)
		self.dealer_hand = Hand()
		self.player_hands = []
		
		self.player_threshold = player_threshold #Threshold for players to stop hitting. 17 by default.
		self.dealer_threshold = dealer_threshold #Threshold for dealer to stop hitting. 18 by default. 
		self.number_of_games=games
		self.score = 0
			
		for _ in range(self.no_of_other_players):	
			self.player_hands.append(Hand())
		
	def card_counter(self,hand):
		
		total_value = 0
		
		for i in hand.get_hand():
			flag=0
			if (hand.get_count())>2:
				flag=1
			face = i[0][0]
			card_value = 0
			if(face.isdigit()==True):
				card_value = int(face)
			elif(face=="J" or face=="Q" or face=="K"):
				card_value = 10
			elif(face=="A"):
				if flag==1:
					card_value = 1
				elif total_value<=21:
					card_value = 11
				else:
					card_value = 1
			else:
				raise Exception("Card value error!")
			total_value = total_value + card_value
			
		return total_value
		
	def score_keeper(self,player_hand_value,dealer_hand_value):
		if(player_hand_value>21 and dealer_hand_value<=21): #You bust
			self.score = self.score - 1
		elif(player_hand_value<=21 and dealer_hand_value>21): #The dealer busts
			self.score = self.score + 1
		elif(player_hand_value>21 and dealer_hand_value>21): #Both bust
			self.score = self.score
		elif(dealer_hand_value>player_hand_value):
			self.score = self.score - 1
		elif(dealer_hand_value<player_hand_value):
			self.score = self.score + 1
			
		print("\nNet Results:")
			
		if(self.score>0):
			print("You won by +%d" %(self.score))
		elif(self.score==0):
			print("It's a draw (+0)")
		elif(self.score<0):
			print("You lost by %d" %(self.score))
		else:
			Raise("Outcome error!")
			
		print("####################################################################################################")
		
	def play(self):
		deck = Deck(self.number_of_games,self.no_of_players)
		deck.shuffle()
		for i in range(self.number_of_games):
			print("Game %d:\n" %(i+1))
			dealer_hand_value = 0
			player_hand_value = 0
			player_hands_value = []
			
			self.dealer_hand.add_hand(deck.draw())
			
			for _ in range(self.no_of_other_players):
				player_hands_value.append(0)
				self.player_hands[_].add_hand(deck.draw())
			
			for _ in range(self.no_of_other_players):
				player_hands_value[_] = self.card_counter(self.player_hands[_])
				while player_hands_value[_]<self.player_threshold:
					self.player_hands[_].add_hand(deck.draw())
					player_hands_value[_] = self.card_counter(self.player_hands[_])
				if(_==0):
					print("\nYou (Player %d) draw %d:" %(_+1,player_hands_value[_]))
				else:
					print("\nPlayer %d draws %d:" %(_+1,player_hands_value[_]))
				print(self.player_hands[_].get_hand())
				#print("Total: %d" %player_hands_value[_])
			
			#print(self.dealer_hand.get_hand())
			dealer_hand_value = self.card_counter(self.dealer_hand)
			#print(dealer_hand_value)
			while dealer_hand_value<self.dealer_threshold:
				self.dealer_hand.add_hand(deck.draw())
				dealer_hand_value = self.card_counter(self.dealer_hand)
			print("\nThe Dealer (Player %d) draws %d:" %(self.no_of_players,dealer_hand_value))
			print(self.dealer_hand.get_hand())
			#print("Total: %d" %dealer_hand_value)
			
			player_hand_value = player_hands_value[0]
			self.score_keeper(player_hand_value,dealer_hand_value)
			self.dealer_hand.clear_hand()
			
			for _ in range(self.no_of_other_players):
				self.player_hands[_].clear_hand()
			
blackjack = Blackjack() #Blackjack(players=4,games=10,player_threshold=17,dealer_threshold=18)
blackjack.play()





