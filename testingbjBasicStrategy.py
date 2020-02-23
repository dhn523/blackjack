'''
TESTING FOR BLACKJACK
---------------------
This file captures the various test cases for bjBasicStrategy 
'''

from bjBasicStrategy import *

def uniTest(unitTest, testText):
	print("="*len(testText),"\n")
	print("UNIT TEST {}\n".format(unitTest),testText,"\n")
	print("="*len(testText))


if __name__ == '__main__':

	uniTest(1, "Multi deck creation")
	'''
	TEST multi deck creations
	'''
	playDeck = Deck(1)
	deck = playDeck.getDeck()
	multiDeck = Deck(2)
	multideck = multiDeck.getDeck()
	print(deck)

	uniTest(2, "One suit (can specific is second for) from the deck, should return 13 elements of 1 suit 1-13")
	'''
	TEST one suit (can specific is second for) from the deck, should return 13 elements of 1 suit 1-13
	'''
	for i in range(1,52*1,4):
		print(deck[i])
	for i in range(1,52):
		tempCard = deck[i]
		if tempCard[0] == 'H':
			print(deck[i])

	uniTest(3, "All suits, should produce 52 cards for a single deck")
	'''
	TEST all suits, should produce 52 cards for a single deck
	'''
	for suit in ['H','S','C', 'D']:
		suitCount = 0
		for i in range(1,53):
			tempCard = deck[i]
			if tempCard[0] == suit:
				suitCount += 1
				print(deck[i])
		print("Suit count for suit {} is {}".format(suit, suitCount))

	uniTest(4, "Card count, below should return -2, -2, 1 respectively")
	# TEST card count, below should return -2, -2, 1 respectively
	print(playDeck.countCards([(1,2),(1,11),(1,10),(1,11)]))			# Adds -2 (+1,-1,-1,-1)
	print(playDeck.countCards([(1,2),(1,4),(1,10),(1,11)]))				# Adds 0 (+1,+1,-1,-1)
	print(playDeck.countCards([(1,2),(1,5),(1,3),(1,4),(1,7),(1,11)]))	# Adds 3 (+1,+1,+1,+1,0,-1)

	uniTest(5, "Make sure that each draw order is random, and how random")
	'''
	TEST make sure that each draw order is random, and how random
	'''
	for q in range(0,5):
		testDeck1 = Deck(2)
		testDeckOrder1 = []
		testDeck2 = Deck(2)
		testDeckOrder2 = []
		testDeck3 = Deck(2)
		testDeckOrder3 = []
		for i in range(1,105):
			testDeckOrder1.append(testDeck1.draw())
			testDeckOrder2.append(testDeck2.draw())
			testDeckOrder3.append(testDeck3.draw())

		if (testDeckOrder1 == testDeckOrder2) or (testDeckOrder2 == testDeckOrder3) or (testDeckOrder1 == testDeckOrder3):
			print("Decks are similar")

		print("Decks 1 and 2 are {} similar.".format(similarityPercent(testDeckOrder1,testDeckOrder2)))
		print("Decks 1 and 3 are {} similar.".format(similarityPercent(testDeckOrder1,testDeckOrder3)))
		print("Decks 2 and 3 are {} similar.".format(similarityPercent(testDeckOrder2,testDeckOrder3)))
		print("Average similarity is: {}".format((similarityPercent(testDeckOrder1,testDeckOrder2)+
			similarityPercent(testDeckOrder1,testDeckOrder3)+
			similarityPercent(testDeckOrder2,testDeckOrder3))/3))

	testDeck1 = Deck(1)
	testDeckOrder1 = []
	testDeckOrder2 = []
	for i in range(0,52):
		testDeckOrder1.append(testDeck1.draw())
	if testDeck1.draw() == 0:
		testDeck1.shuffle()
	for i in range(0,52):
		testDeckOrder2.append(testDeck1.draw())
	print("Decks 1 and 2 are {} similar.".format(similarityPercent(testDeckOrder1,testDeckOrder2)))

	uniTest(6, "Automatic shuffle")
	'''
	TEST that the deck automatically gets shuffle after drawing
	'''
	playDeck = Deck(1)
	deck = playDeck.getDeck()
	
	i = 0
	while i <157:
		playDeck.draw()
		i+=1
