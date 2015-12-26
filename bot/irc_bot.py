import math
import random

class vote:
	def __init__(self,myManager,callback):
		self.peopleVoting = [] #people allowed to vote
		self.choices = [] #list of voteOptions available to vote for
		self.onFinish = callback #a function taking a list of choices
		self.manager = myManager #a reference to the manager in which this vote is contained

	def createBinaryChoice(self):
		self.choices = [voteOption("yes"),voteOption("no")]

	def runVote(self):
		voterIndex = len(self.peopleVoting) - 1
		choiceIndex = 0
		while(voterIndex >= 0):
			print self.peopleVoting[voterIndex], "make your choice!"
			cur_input = raw_input(">> ")
			while(choiceIndex < len(self.choices)):
				if(cur_input == self.choices[choiceIndex].name):
					self.choices[choiceIndex].votes += 1
					self.peopleVoting.pop(voterIndex)
					voterIndex -= 1
					break
				choiceIndex += 1
			if(choiceIndex >= len(self.choices)):
				print "Invalid choice, choose again!"
				choiceIndex = 0
		self.onFinish(self.choices)

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
				personIndex = 0
				while personIndex < len(self.people):
					if(self.people[personIndex].name == cur_input):
						print "Name is already taken!"
						break
					personIndex += 1
				if(personIndex >= len(self.people)):
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
		while(self.isQuit == False):
			self.gameLoop()

	def gameLoop(self):
		self.runDay()
		self.runNight()
		self.dayNumber += 1

	def runDay(self):
		print "Day has broken!"
		if(self.dayNumber != 0):
			#set up and run kill vote
			killVote = vote(self,self.resolveKillVote)
			for person in self.people:
				if person.isDead == False:
					killVote.choices.append(voteOption(person.name))
					killVote.peopleVoting.append(person.name)
			print "Time to vote on whom we would like to kill!"
			killVote.runVote()

			#do stuff that you don't do on the first day in Mafia
			#i.e. execution of suspected mafia / werewolf
		#else:
			#self.runFirstDay()

	#def runFirstDay(self):


	def runNight(self):
		print "Night has fallen!"
		werewolfVote = vote(self, self.resolveKillVote)
		for person in self.people:
			if(person.type == "Werewolf" and person.isDead == False):
				werewolfVote.peopleVoting.append(person.name)
			elif(person.isDead == False):
				werewolfVote.choices.append(voteOption(person.name))
		print "Werewolves, choose your victims!"
		werewolfVote.runVote()

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

	def voteCount(self,choices):
		for choice in choices:
			print choice.name, "has", choice.votes, "votes!"
		self.isQuit = True

bot = manager()
bot.startGame()
