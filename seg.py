import os
import time
import random

# A City class, built like a grid to contain numerous Person objects
class City():
	def __init__(self, width, height, density, numRaces):
		self.housing = []
		self.free_houses = []
		self.number_races = numRaces
		self.width = width
		self.height = height
		self.generate(width,height, density)
		self.initial = list([[citizen for citizen in row] for row in self.housing])
		

	# Generates a grid with a set width, height and density of people. Future iterations should include a psuedo-random version.
	def generate(self, width, height, density):
		for i in range(height):
			self.housing.append([])
			self.housing[i].extend([Person(j % self.number_races,i,j) for j in range(int(width*density))])
			self.housing[i].extend([None for j in range(width - int(width*density))])
			self.free_houses.extend([[i,j] for j in range(int(width*density),width)])
		return True

	# Crude way to print
	def printMap(self, map_to_print, clear):
		if clear:
			print(chr(27) + "[2J")
		
		for row in map_to_print:
			line = str()
			for citizen in row:
				if citizen == None:
					line += "+ " # Free houses are printed as a +
				else:
					line += str(citizen.getRace()) + " "
			print line
		return True

	# Main method in City, taes care of updating the happiness of each Person and moving them if neccessary
	def Update(self):
		housing = list(self.housing)
		equilibrium = False
		for row in housing:
			for citizen in row:
				if citizen != None: #Check there is a citizen at this grid point
					citizen.calcHappiness(self.nearbyHouses(citizen))
					if citizen.getHappiness() < 0: 
						self.movePerson(citizen)
						equilibrium = True
		return equilibrium

	def run(self, increment):
		changeCount = 0
		while self.Update():
			changeCount += 1
			self.printMap(self.housing, True)
			time.sleep(increment)

		print "\nVs. Initial map: "
		self.printMap(self.initial, False)
		print "\n\n It took " + str(changeCount) + " changes for equilibrium to be reached."
		return True

	def nearbyHouses(self, citizen):
		x,y = citizen.getLocation()

		if x ==0:
			if y == 0:
				return [self.housing[0][1], self.housing[1][0]]
			elif y == self.height - 1:
				return [self.housing[0][y - 1], self.housing[1][y]]
			else:
				return [self.housing[0][y-1],self.housing[0][y+1],self.housing[x+1][y]]
		elif x == self.width - 1:
			if y == 0:
				return [self.housing[x][1], self.housing[x-1][0]]
			elif y == self.height - 1:
				return [self.housing[x][y - 1], self.housing[x-1][y]]
			else:
				return [self.housing[x][y-1], self.housing[x][y+1], self.housing[x-1][y]]
		else:
			if y == 0:
				return [self.housing[x][1], self.housing[x-1][0], self.housing[x+1][0]]
			elif y == self.height - 1:
				return [self.housing[x][y - 1], self.housing[x-1][y], self.housing[x+1][y]]
			else:
				return [self.housing[x][y-1], self.housing[x][y+1], self.housing[x-1][y], self.housing[x+1][y]]

		



	def movePerson(self, citizen):
		#Picks a new house randomly for those that are free
		houseNumber = random.randint(0,len(self.free_houses)-1)
		newHome = self.free_houses[houseNumber]
		del self.free_houses[houseNumber]

		oldHome = citizen.getLocation()
		self.housing[oldHome[0]][oldHome[1]] = None
		self.free_houses.append(oldHome)
		self.housing[newHome[0]][newHome[1]] = citizen
		citizen.moveMe(newHome[0], newHome[1])
		return True


class Person():
	def __init__(self, race, x, y):
		self.race = race
		self.happiness = 0
		self.coord = [x,y]

	def getRace(self):
		return self.race

	def getHappiness(self):
		return self.happiness

	def getLocation(self):
		return self.coord

	def moveMe(self,x,y):
		self.coord = [x,y]
		return True

	def calcHappiness(self, otherHouses):
		self.happiness = 0
		for house in otherHouses:
			if house == None:
				self.happiness -= 0.75
			else:
				otherRace = house.getRace()
				if otherRace < self.race:
					self.happiness -= 1
				elif otherRace == self.race:
					self.happiness += 1
				elif otherRace == self.race +1:
					self.happiness += 0.5
				else:
					self.happiness -= int((otherRace-self.race)/2 + 1)
		return True


# Defines a City with width, height, density (of filled housing) and number of races
c = City(10, 10, 0.8, 4)
#runs the city simulation with time increments in seconds
c.run(1)
