import math
import random

class vote:
	def __init__(self,callback):
		self.peopleVoting = [] #people allowed to vote
		self.choices = [] #list of voteOptions available to vote for
		self.onFinish = callback #a function taking a list of choices 

	def createBinaryChoice(self):
		self.choices = [voteOption("yes"),voteOption("no")]

class voteOption:
	def __init__(self, name):
		self.name = name
		self.votes = 0

class person:
	def __init__(self, name):
		self.name = name #string
		self.type = "Villager" # "Villager" / "Werewolf"
		self.isChief = False #boolean
		self.lover = None #another player or None 
		self.isDead = False #boolean

_PLAYERS_TO_START_GAME_ = 3

class manager:
	def __init__(self):
		self.isDay = True
		self.dayNumber = 0
		self.isQuit = False #has the game quit?
		self.people = [] #LIST of people

	def setupGame(self):
		#Gets input and adds players accordingly
		ready = False
		while (ready == False):
			print "There are currently", len(self.people), "players in the game."
			if(len(self.people) < _PLAYERS_TO_START_GAME_):
				print "Too few players to begin game."
				print "Type your name, or quit to quit."
			else:
				print "Type your name, begin to start game, or quit to quit."
			cur_input = raw_input(">> ")
			
			if(cur_input == "quit"):
				self.isQuit = True
				ready = True
			elif(len(self.people) >= _PLAYERS_TO_START_GAME_ and cur_input == "begin"):
				ready = True
			else:
				new_person = person(cur_input)
				self.people.append(new_person)
				print "Person", new_person.name, "added." 

		#Set up players with correct classes (werewolves / villagers)
		num_werewolves = round(len(self.people) / 3)
		while (num_werewolves > 0):
			choice = int(math.floor(random.random() * len(self.people)))
			if(self.people[choice].type != "Werewolf"):
				self.people[choice].type = "Werewolf"
				num_werewolves -= 1
				print self.people[choice].name, "is now a werewolf!"


	def startGame(self):
		self.setupGame()
		#while(self.isQuit == False):
			#self.gameLoop()

	#def gameLoop(self):
		#self.runDay()
		#self.runNight()

	#def runDay():


	#def runNight():

	#killVote = vote(resolveKillVote)

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
				print person.name , "is dead!"

bot = manager()
bot.startGame()