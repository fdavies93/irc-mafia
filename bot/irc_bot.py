import math
import random
import os
import platform

class vote:
	def __init__(self,myManager,callback):
		self.peopleVoting = [] #people allowed to vote
		self.choices = [] #list of voteOptions available to vote for
		self.onFinish = callback #a function taking a list of choices
		self.hasSpoofing = False
		self.voterMessage = ""
		self.nonVoterMessage = ""
		#is private?
		self.manager = myManager #a reference to the manager in which this vote is contained

	def createBinaryChoice(self):
		self.choices = [voteOption("yes"),voteOption("no")]

	def runVote(self):
		#isVoter = False
		choiceAccepted = False
		#choiceIndex = 0
		for person in self.manager.people:
			isVoter = False
			for voter in self.peopleVoting:
				if(voter == person):
					isVoter = True
			if(isVoter and person.isDead == False):
				self.manager.interface.sendMessageToPlayer(self.voterMessage, person)
				while(choiceAccepted == False):
					player_input = self.manager.interface.waitForMessageFromPlayer(person)
					choiceIndex = 0
					while(choiceIndex < len(self.choices)):
						if(player_input.message == self.choices[choiceIndex].name):
							self.choices[choiceIndex].votes += 1
							choiceAccepted = True
						choiceIndex += 1
					if(choiceAccepted == False):
						self.manager.interface.sendMessageToPlayer("That choice is not valid, choose again.")
			elif(isVoter == False and self.hasSpoofing and person.isDead == False):
				self.manager.interface.sendMessageToPlayer(self.nonVoterMessage, person)
		self.onFinish(self.choices)

class voteOption:
	def __init__(self, name):
		self.name = name
		self.votes = 0

class person:
	def __init__(self, name):
		self.name = name #string
		self.type = "Villager" # "Villager" / "Werewolf" / "WitchDoctor"
		self.isChief = False #boolean
		self.lover = None #another player or None
		self.isDead = False #boolean

_PLAYERS_TO_START_GAME_ = 3

class abstractInterface:
	def __init__(self,myManager):
		self.hostname = ""
		self.port = 6667
		self.nick = "bot"
		self.manager = myManager
	def connect(self):
		return
	def setupGame(self):
		return
	def sendMessageToAll(self, message):
		return
	def sendMessageToPlayer(self, message, player):
		return
	#send message to people
	def waitForMessageFromPlayer(self, player):
		#wait for private message and public message from player x
		return
	def parseMessage(self, message):
		return

class messageData:
	def __init__(self, message, sender):
		self.message = message
		self.sender = sender

class consoleInterface(abstractInterface):
	def setupGame(self):
		ready = False
		while (ready == False):
			self.sendMessageToAll("There are currently " + str(len(self.manager.people)) + " players in the game.")
			if(len(self.manager.people) < _PLAYERS_TO_START_GAME_):
				self.sendMessageToAll("Too few players to begin game.")
				self.sendMessageToAll("Type your name, or quit to quit.")
			else:
				self.sendMessageToAll("Type your name, or begin to start game.")
			cur_input = self.waitForMessage().message
			#############################
			#make quit not an option
			if(len(self.manager.people) >= _PLAYERS_TO_START_GAME_ and cur_input == "begin"):
				ready = True
			#this should be changed so that you need to ask all players' permission
			#before you start the game
			#CHANGE WHEN IMPLEMENTING IRC
			else:
				personIndex = 0
				while personIndex < len(self.manager.people):
					if(self.manager.people[personIndex].name == cur_input):
						self.sendMessageToAll("Name is already taken!")
						break
					personIndex += 1
				if(personIndex >= len(self.manager.people)):
					new_person = person(cur_input)
					self.manager.people.append(new_person)
					self.sendMessageToAll("Person "+new_person.name+" added.")
		########################################################

	def sendMessageToAll(self, message):
		print message

	def sendMessageToPlayer(self, message, player):
		print "Please get", player.name, "to come to the keyboard."
		raw_input("Press Enter when ready.")
		self.clearConsole()
		print message
		raw_input("Press Enter to clear.")
		self.clearConsole()

	def waitForMessage(self):
		messageToReturn = messageData(raw_input(">> "), None)
		return messageToReturn

	def waitForMessageFromPlayer(self, player):
		messageToReturn = messageData(raw_input(">> "), player)
		return messageToReturn

	def clearConsole(self):
		sysName = platform.system()
		if(sysName == "Windows"):
			os.system('cls')
		else:
			os.system('clear')

class ircInterface(abstractInterface):
	def sendMessageToAll(self, message):
		return

class manager:
	def __init__(self):
		self.isDay = True
		self.dayNumber = 0
		self.isQuit = False #has the game quit?
		self.people = [] #LIST of people
		self.interface = consoleInterface(self)
	def setupGame(self):
		ready = False
		self.interface.setupGame()
		#Set up players with correct classes (werewolves / villagers)
		num_werewolves = round(len(self.people) / 3)
		while (num_werewolves > 0):
			choice = int(math.floor(random.random() * len(self.people)))
			if(self.people[choice].type != "Werewolf"):
				self.people[choice].type = "Werewolf"
				num_werewolves -= 1
				#print self.people[choice].name, "is now a werewolf!"

		#add code so it tells everyone what they are
		for player in self.people:
			self.interface.sendMessageToPlayer("You are a " +player.type+"!",player)
		self.interface.sendMessageToAll("Prepare to play Werewolf!")

	def startGame(self):
		self.setupGame()
		while(self.isQuit == False):
			self.gameLoop()

	def gameLoop(self):
		if (self.isQuit == False):
			self.runDay()
		if (self.isQuit == False):
			self.runNight()
			self.dayNumber += 1

	def runDay(self):
		self.interface.sendMessageToAll("Day has broken!")
		if(self.dayNumber != 0):
			#set up and run kill vote
			killVote = vote(self,self.resolveKillVote)
			killVote.voterMessage = "Choose who you think is the werewolf."
			for person in self.people:
				if person.isDead == False:
					killVote.choices.append(voteOption(person.name))
					killVote.peopleVoting.append(person)
			self.interface.sendMessageToAll("Time to vote on whom we would like to kill!")
			killVote.runVote()
			self.testForVictory()
			#do stuff that you don't do on the first day in Mafia
			#i.e. execution of suspected mafia / werewolf
		#else:
			#self.runFirstDay()

	#def runFirstDay(self):


	def runNight(self):
		self.interface.sendMessageToAll("Night has fallen!")
		werewolfVote = vote(self, self.resolveKillVote)
		werewolfVote.voterMessage = "Who would you like to kill?"
		werewolfVote.nonVoterMessage = "Stay asleep, sheeple."
		werewolfVote.hasSpoofing = True
		for person in self.people:
			if(person.type == "Werewolf" and person.isDead == False):
				werewolfVote.peopleVoting.append(person)
			elif(person.isDead == False):
				werewolfVote.choices.append(voteOption(person.name))
		#for person in self.people:
		#	if(person.type == "Werewolf"):
		#		self.interface.sendMessageToPlayer("Werewolf, choose your victim!", person)
		#	else:#generic villager message
		#		self.interface.sendMessageToPlayer("Villager, stay asleep and await the slaughter!", person)
		werewolfVote.runVote()
		self.testForVictory()

	def testForVictory(self):
		numWerewolves = 0
		numVillagers = 0
		for person in self.people:
			if(person.type == "Villager" and person.isDead == False):
				numVillagers += 1
			elif(person.type == "Werewolf" and person.isDead == False):
				numWerewolves += 1
		if(numWerewolves == 0):
			self.interface.sendMessageToAll("Game over, villagers win!")
			self.isQuit = True
		elif(numVillagers == 0):
			self.interface.sendMessageToAll("Game over, werewolves win!")
			self.isQuit = True

	# This is dramatic!
	def resolveKillVote(self,choices):
		votesToKill = 0
		personToKill = ""

		for choice in choices:
			if(choice.votes > votesToKill):
				personToKill = choice.name
				votesToKill = choice.votes

			#needs a thing to deal with equal votes for same person

		for person in self.people:
			if(person.name == personToKill):
				person.isDead = True #DRAMA
				self.interface.sendMessageToAll(person.name + "is dead!")

	def voteCount(self,choices):
		for choice in choices:
			print choice.name, "has", choice.votes, "votes!"
		self.isQuit = True

bot = manager()
bot.startGame()
