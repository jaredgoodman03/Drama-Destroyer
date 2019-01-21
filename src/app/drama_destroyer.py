import os
from app import app
from flask import Flask, request, render_template
from app.forms import LoginForm

class Couple:
	def __init__(self, first, second):
		self.first = first
		self.second = second

	def __str__(self):
		return self.first + " & " + self.second

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return isinstance(other, Couple) and (self.first == other.first and self.second == other.second) or (self.first == other.second and self.second == other.first)

	def __hash__(self):
		return hash((self.first, self.second))

	def contains(self, other):
		return other == self.first or other == self.second

	def match(self, other):
		if (other == self.first):
			return self.second
		if (other == self.second):
			return self.first
		print("Match not found!")
		return ""

	def switcharoo(self, cheater, other):
		if (cheater == self.first):
			self.second = other # Mr steal ur girl
		elif (cheater == self.second):
			self.first = other

class Destroyer: # This sounds a lot edgier than it actually is
	def __init__(self):
		files = os.listdir("profiles")

		self.people = dict()
		for person in files:
			self.people[person] = list(filter(None, open("profiles/" + person, "r").read().split("\n")))

		for person in self.people:
			for choice in self.people[person]:
				if choice not in self.people:
					self.people[person].remove(choice)

		print(self.people)

		self.couples = set()

	def taken(self, person):
		for couple in self.couples:
			if (couple.contains(person)):
				return True
		return False

	def prefers(self, cheater, other):
		for couple in self.couples:
			if (couple.contains(cheater)):
				cheated = couple.match(cheater)
				ranking = self.people[cheater]
				try:
					if ranking.index(cheated) > ranking.index(other):
						return True
					else:
						return False
				except:
					return False

	def getCouple(self, person):
		for couple in self.couples:
			if couple.contains(person):
				return couple
		return False

	def iterate(self, person):
		for choice in self.people[person]:
			if self.taken(choice):
				if self.getCouple(choice).contains(person):
					return
				if self.prefers(choice, person):
					couple = self.getCouple(choice)
					self.couples.remove(couple)
					self.couples.add(Couple(choice, person))
					try:
						self.iterate(couple.match(choice))
					except RecursionError:
						print("Oopsie whoopsie! We made a fucky wucky! A little fucko boingo! The code monkeys at our headquawters are working VERY HAWD to fix this! uwu")
						self.couples.add(Couple(choice, person))
					return
			else:
				try:
					if person in self.people[choice]:
						if self.taken(person):
							self.couples.remove(self.getCouple(person))
						self.couples.add(Couple(choice, person))
				except:
					self.people[person].remove(choice)

def fixCapitalization(rope):
	words = rope.split(" ")
	toReturn = ""
	for word in words:
		if len(word) > 1:
			toReturn += (word[0].upper() + word[1:] + " ")
	return toReturn[:len(toReturn) - 1]

@app.route('/results')
def results():
	d = Destroyer()
	for person in d.people:
		d.iterate(person)
	return render_template('results.html', couples=(d.couples), title="This year's TOLO couples")

@app.route('/entry')
def entry():
	return render_template('entry.html', title="Enter your rankings")

@app.route('/entry', methods=['POST'])
def entry_post():
	name = fixCapitalization(request.form['name'])
	ranking = request.form['ranking']
	print("Name: " + name)
	rankinglist = ranking.split("\n")
	#print("Ranking: " + (str) rankinglist)
	if name == "":
		return render_template('entry.html', title="Enter your rankings", error="This field is required.")
	if name in os.listdir("profiles"):
		return render_template('oopsie.html', title="An error occured")
	with open("profiles/" + name, "w+") as file:
		for choice in rankinglist:
			file.write(fixCapitalization(choice) + "\n")
	return render_template('thankyou.html', title="Submitted successfully", name=name)

@app.route('/names')
def names():
	return render_template("names.html", title="Names", names=os.listdir("profiles"))

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html", title="Home")
