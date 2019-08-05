# Black Jack Basic Strategy

import time
import random
import matplotlib.pyplot as plt 

start_time = time.time()

def similarityPercent(L1, L2):
	'''
	Returns the percentage that 2 lists are similar
	'''
	list1 = L1
	list2 = L2
	similarityPercent = 0
	for i in range(len(list1)):
		if list1[i] == list2[i]:
			similarityPercent += 1
	return similarityPercent/len(list1)

def plotCount(deckNum):
	'''
	Plots the count for certain number of decks for blackjack play
	'''	
	# x axis values 
	x = [] 
	# corresponding y axis values 
	y = []

	testDeck1 = Deck(deckNum)
	testDeckOrder1 = []
	
	for i in range(0,52*deckNum):
		card = testDeck1.draw()
		x.append(i)
		count = testDeck1.getCount()
		y.append(count)
	  
	#plotting the points  
	plt.plot(x, y) 
	# naming the x axis 
	plt.xlabel('Card Draw') 
	# naming the y axis 
	plt.ylabel('Count') 
	# giving a title to my graph 
	plt.title('Count Over Card Draw') 
	# function to show the plot 
	plt.show() 


class Deck(object):
    def __init__(self, numDecks):
    	suits = ['H','S','C', 'D']
    	# Numbers in a suit, Ace = 1, Jack = 11, Queen = 12, King = 13
    	temp = {}

    	for i in range(0, numDecks*52):
    		temp_suit = suits[i%len(suits)]		# Mod of 4 will iterate through the 4 suits
    		temp_num = i%13						# Mod of 13 will iterate through the 13 numbers, need to +1 to get range 1-13
    		temp[i+1] = (temp_suit, temp_num+1)

    	self.originalDeck = temp.copy() 		# Keep this deck when the play deck runs out
    	self.playDeck = temp.copy()  			# This deck can be altered
    	self.count = 0

    def getDeck(self):
    	'''
    	Returns the deck in play
    	'''
    	return self.playDeck

    # Keeps the count for the deck, takes in the cards played
    def countCards(self, playedCards):
    	'''
		Returns the current count for the deck
    	'''
    	for card in playedCards:
    		cardValue = card[1]
    		# Increase the count when lower cards drawn
    		if cardValue in range(2,6):
    			self.count = self.count + 1
    		elif cardValue in range(10,13) or cardValue == 1:
    			self.count = self.count - 1

    	return self.count

    def getCount(self):
    	return self.count

    def shuffle(self):
    	'''
		This function "shuffles" the deck, but it will resets the deck to the original
    	'''
    	self.count = 0
    	tempDeck = self.originalDeck
    	self.playDeck = tempDeck.copy()
    
    def draw(self):
    	'''
    	Returns a card from the deck and removes that card from the deck
    	'''
    	# If the deck has run out of cards, shuffle the deck
    	if len(self.playDeck) == 0:
    		print("Reshuffling deck")
    		self.shuffle()
    	remainingCards = []
    	remainingCards = list(self.playDeck.keys())
    	cardSelect = random.choice(remainingCards)
    	card = self.playDeck[cardSelect]
    	self.countCards([card])
    	del(self.playDeck[cardSelect])
    	return card

class Participant(object):
	def __init__(self, deckNum, participants):
		self.playDeck = Deck(deckNum)
		self.dealer = {
			'hand': [],
			'wins': 0,
			'faceCard': 0
		}
		self.participants = {}
		player = {
			'wins': 0,
			'hand': []
		}
		for i in range(1, participants+1):
			playerNum = "P"+str(i)
			self.participants[playerNum] = player.copy()

	def getDeckAtrributes(self):
		return {
			'count': self.playDeck.getCount(),
			'length': len(self.playDeck.getDeck())
		}

	def players(self):
		'''
		Returns the players in the game
		'''
		return self.participants.keys()

	def getPlayers(self):
		'''
		Returns the players and their hands
		'''
		return self.participants.copy()

	def getPlayHand(self, player):
		'''
		Returns the hand value for a specific player
		'''
		return self.participants[player]['hand']

	def getDealer(self):
		return self.dealer.copy()

	def cardVal(self, card):
		'''
		This function returns the value of the card as an array
		'''
		value = card[1]
		if value > 10:
			return [10]
		elif value == 1:
			return [1, 11] 	
		else:
			return [card[1]]


	def drawHandsAll(self):
		'''
		This function draws hands for all the participants, including the dealer going last 
		'''
		# First round of cards
		tempHand = []
		for p in list(self.participants.keys()):
			card = self.playDeck.draw()
			value = self.cardVal(card)
			self.participants[p]['hand'] = value

		card = self.playDeck.draw()
		value = self.cardVal(card)
		self.dealer['hand'] = value
		self.dealer['faceCard'] = value.copy()

		# Second Round of Cards
		participants = list(self.participants.keys())
		participants.append('dealer')
		for p in participants:
			if p == 'dealer':
				tempHand = self.dealer['hand']
			else:
				tempHand = self.participants[p]['hand']
			card = self.playDeck.draw()
			value = self.cardVal(card)
			if len(tempHand)==1 and len(value)==1:
				tempHand[0]= tempHand[0]+value[0]
				
			elif len(tempHand)==1 and len(value)>1:
				value[0]= value[0]+tempHand[0]
				value[1]= value[1]+tempHand[0]
				tempHand = value.copy()
			# If the first card was an ace it should just add 1 to each
			elif len(tempHand) > 1:
				tempHand[0]= tempHand[0]+value[0]
				tempHand[1]= tempHand[1]+value[0]
			if p == 'dealer':
				self.dealer['hand'] = tempHand.copy()
			else:
				self.participants[p]['hand'] = tempHand.copy()


	def checkBust(self, player):
		'''
		This function checks if the player has busted, returns True if busted
		'''
		if player[0] == "P":
			Hand = self.participants[player]['hand']
		else:
			Hand = self.dealer['hand']
		
		if Hand[0] > 21:
			print("BUST")
			return True
		else:
			return False


	def hit(self, player):
		'''
		Draws a card and changes the value of the hand
		'''
		playerHand = self.participants[player]['hand']
		card = self.playDeck.draw()
		print("Hit card: ",card)
		cardVal = self.cardVal(card)

		if len(playerHand) == 2:
			playerHand[0] = playerHand[0] + cardVal[0]
			playerHand[1] = playerHand[1] + cardVal[0]
		elif len(cardVal) == 2:
			playerHand.append(playerHand[0]+cardVal[1])
			playerHand[0] = playerHand[0] + cardVal[0]
		else:
			playerHand[0] = playerHand[0] + cardVal[0]

		self.participants[player]['hand'] = playerHand.copy()

	def dealerHit(self):
		'''
		Draws a card and changes the value of the Dealer's hand
		NOTE: DEALER STANDS ON SOFT 17 (If they get Ace and 6, they stand)
		'''
		dealerHand = self.dealer['hand']

		while dealerHand[len(dealerHand)-1] < 17:
			card = self.playDeck.draw()
			print("Hit card: ",card)
			cardVal = card[1]
			if cardVal > 10:
				cardVal = 10

			if len(dealerHand) == 2:
				dealerHand[0] = dealerHand[0] + cardVal
				dealerHand[1] = dealerHand[1] + cardVal
			else:
				dealerHand[0] = dealerHand[0] + cardVal

		if len(dealerHand) == 2 and dealerHand[1] > 21:
			while dealerHand[0] < 17:
				card = self.playDeck.draw()
				print("Hit card: ",card)
				cardVal = card[1]
			if cardVal > 10:
				cardVal = 10
			dealerHand[0] = dealerHand[0] + cardVal			
		
		self.dealer['hand'] = dealerHand.copy()

	def playerWins(self, player):
		'''
		This function adds wins to a players profile
		'''
		self.participants[player]['wins'] = self.participants[player]['wins'] + 1 




def basicStrategy(phand, dealerFace):
	'''
	TODO
	This function will take in the player hand and the Dealer's face up card to determine if player should hit, double down or stand
	'''
	# Should function distinguish between hit and DD
	# Use hand len to det if ace (if 2 values then there's an ace)
	if phand[0] < 17:
		return True
	else:
		False



if __name__ == '__main__':
	# part = Participant(2,3)

	# TEST Setting up the participants
	# print(part.getPlayers())
	# print(part.getDealer())

	# TEST check that the card value is sent correctly
	# print(part.cardVal(('A',1)))
	# print(part.cardVal(('3',3)))
	# print(part.cardVal(('J',10)))

	# TEST Hit for a participant
	# part.hit('P3')
	# part.hit('P2')
	# print(part.getPlayers())

	# TEST drawing a hand
	# part.drawHandsAll()
	# print("Players hands", part.getPlayers())
	# print("Dealer Hand", part.getDealer())

	# TEST Dealer hitting until bust or 17
	# part.dealerHit()
	# print("Dealer hand post hit", part.getDealer())

	# TEST Bust Check on a hit

	# part.hit('P2')
	# print(part.checkBust('P2'))
	# if part.checkBust('P2'):
	# 	print("Bust on first hit")
	# testHit2 = part.hit('P2')
	# if part.checkBust('P2'):
	# 	print("Bust on second hit")

	# TEST Hitting until bust
	# for p in list(part.players()):
	# 	while not(part.checkBust(p)):
	# 		part.hit(p)
	# 	print(part.getDeckAtrributes())


	# print("Bust on: ", testHit)
	# print("Players hands post hit", part.getPlayers())

	# TODO Implement game
	'''
	Draw cards for everyone
	Start with P1 then to n
	Send players card to basicStrategy
	When you get to the dealer have them take action, call function
	TODO make winner function
		If the player hand is > than dealer AND not over 21, 1 win
		If 21 player wins the hand TODO check if this applies post hit or on draw
	'''

	players = Participant(2,3)
	players.drawHandsAll()
	print(players.getPlayers())
	print(players.getDealer())
	dealer = players.getDealer()
	for p in list(players.players()):
		while basicStrategy(players.getPlayHand(p), dealer['faceCard']):
			players.hit(p)
		print(players.getDeckAtrributes())
	players.dealerHit()
	dealer = players.getDealer()
	for p in list(players.players()):
		if players.checkBust('dealer') and not players.checkBust(p):
			players.playerWins(p)
		elif not players.checkBust(p) and players.getPlayHand(p)[0] > dealer['hand'][0]:
			print(players.getPlayHand(p)[0])
			print(dealer['hand'][0])
			players.playerWins(p)	  
	print(players.getPlayers())
	print(players.getDealer())




	print('\nProgram ran in {} seconds'.format(time.time()-start_time))