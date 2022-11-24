import heapq

"""
General idea:

The program's main function has a preference scale value, a starting location and a finishing location as inputs. The output will be a "tour",
a list containing the locations which have a similar preference scale value that can be walked from the start to the finish location, the 
total time that travelling between the locations will take, and the total time that visiting the locations will take
A "similar" preference value will be defined as a value within 3 points (up or down) on the scale compared to the input of the user. 
Therefore, locations with values in the preference scale further away than 3 points will be discarded.

Special variable definitions:

pref_scale is a scale from 1 to 10 that determines whether the location is more basic sight seeing (1) or more
adventurous (10) based on our classifications.
time_to_visit is defined as the time it takes to visit a location, in minutes.
In class Walk, time_to_travel is defined as the time it takes to go from one location to the other by walking, in minutes.

"""


# We start by defining our basic classes to implement weighted graphs, which will be called Walk(representing Edge) and Location(representing Node)

class Walk():
    registry = []

    def __init__(self, time_to_travel, startVertex, targetVertex):
        self.time_to_travel = time_to_travel
        self.startVertex = startVertex
        self.targetVertex = targetVertex
        self.registry = self.registry.append(self)


class Location():
    registry = []

    def __init__(self, name, pref_scale, time_to_visit):
        self.name = name
        self.pref_scale = pref_scale
        self.time_to_visit = time_to_visit
        self.registry = self.registry.append(self)
        self.visited = False
        self.predecessor = None
        self.adjacencylist = []
        self.minDistance = float("inf")

    # Next, we create methods in the Location class that serve the purpose of finding a path between the nodes

    def __lt__(self, other):  # less than is a "magic method" in python"
        selfPriority = self.minDistance
        otherPriority = other.minDistance
        return selfPriority < otherPriority

    def calculateShortestWalk(self):
        q = []
        startVertex = self
        startVertex.minDistance = 0
        heapq.heappush(q, (startVertex.minDistance, startVertex))
        while q:
            currentVertex = heapq.heappop(q)[1]
            for edge in currentVertex.adjacencylist:
                u = edge.startVertex
                v = edge.targetVertex
                newDistance = u.minDistance + edge.time_to_travel
                if newDistance < v.minDistance:  # __lt__ works here
                    v.predecessor = u
                    v.minDistance = newDistance
                    heapq.heappush(q, (v.minDistance, v))

    def getShortestWalkTo(self, targetvertex):
        total = 0  # total stores the time it takes to visit the locations
        node = targetvertex
        tour = []
        while node is not None:
            total += node.time_to_visit
            tour.append(node.name)  # we append the names of the locations to the tour list
            node = node.predecessor
        tour.reverse()
        print("Your tour is", tour)
        print("Travelling between the locations will take ", targetvertex.minDistance, " minutes in total.")
        print("Visiting the locations will take ", total, " minutes in total.")
        print("Have a nice visit!")


# We are done with the methods, but the most important part of the program remains. Next, we define a function that will modify our Walk instances
# to remove those that do not fit the preference scale requirements. We will update their "time to travel" values and their target destinations.

def remove_non_candidates(prefscale):
    range1 = range((prefscale - 3), (prefscale + 4))
    for walk in Walk.registry:  # iterate through all walk instances
        if walk.targetVertex.pref_scale not in range1:  # if the pref scale of the target vertex of walks is not what we want...
            for walk2 in Walk.registry:  # iterate through walks again!
                if walk2.startVertex == walk.targetVertex:  # find a walk that has a start vertex which is the target vertex of the other walk
                    if len(
                            walk2.targetVertex.adjacencylist) != 0:  # if the adjacency list of our second walk is not empty...
                        walk.targetVertex = walk2.targetVertex  # the target vertex of the initial walk is the target vertex of the second walk
                        walk.time_to_travel += walk2.time_to_travel  # add the time to travel of the second walk to the time to travel of the first
                    else:
                        walk.targetVertex = walk2.startVertex  # if the adjacency list was empty, the target vertex of our initital walk will be the start vertex of the second
        if walk.startVertex.pref_scale not in range1:  # we are also checking for the pref scale of the start vertex of our initial walk
            for walk2 in Walk.registry:  # repeat second iteration
                if walk2.targetVertex == walk.startVertex:  # find a walk that has a target vertex which is the start vertex of the other walk
                    walk.startVertex = walk2.startVertex  # the start vertex of our first walk is the start vertex of our second walk
                    walk.time_to_travel += walk2.time_to_travel  # update time to travel once more


# Essentially, we are iterating through all of the instances of walk (our edges), and updating them to fit our requirements using double loops and if statements

def check_input(prefscale, start, finish):
    if prefscale not in range(1, 11):
        print("Please enter a valid preference scale value! (1-10)")

    if start not in Location.registry:
        print("Please enter a valid start location!")

    if finish not in Location.registry:
        print("Please enter a valid finish location!")


# Basic input checking, in case something goes wrong

def find_tour(prefscale, start, finish):
    range1 = range((prefscale - 3), (prefscale + 4))
    remove_non_candidates(prefscale)
    check_input(prefscale, start, finish)
    if finish.pref_scale in range1:
        start.calculateShortestWalk()
        start.getShortestWalkTo(finish)
    else:  # if the user does not like the pref scale of the finish location, we give a warning message
        x = input(
            "This destiny location does not match your preferences. Are you sure you would like to visit it?: (Yes/No)")
        if x.lower() == "yes":
            start.calculateShortestWalk()
            start.getShortestWalkTo(finish)
        elif x.lower() == "no":
            print("Please enter a different destiny location")
        else:
            print("Please enter a valid input (Yes/No)")


# Simply executing the functions and methods we have defined, given a series of inputs

# Defining locations

Poke = Location("Selfish Poke", 1, 15)
Cathedral = Location("Cathedral", 3, 90)
Alcazar = Location("Alcazar", 4, 100)
Aqueduct = Location("Aqueduct", 3, 20)
Burbuja = Location("Burbuja", 5, 5)
Hills = Location("Hills", 8, 120)
Damasco = Location("Damasco", 8, 50)
Iglesia = Location("Iglesia", 2, 60)
Irish = Location("Irish", 10, 30)
Plaza = Location("Plaza", 8, 60)

# Defining walks

walkPI = Walk(3, Plaza, Irish)
walkPC = Walk(1, Plaza, Cathedral)
walkIA = Walk(8, Irish, Aqueduct)
walkIP = Walk(4, Irish, Poke)
walkPIG = Walk(7, Poke, Iglesia)
walkPA = Walk(7, Poke, Aqueduct)
walkAB = Walk(2, Aqueduct, Burbuja)
walkBD = Walk(14, Burbuja, Damasco)
walkAD = Walk(15, Aqueduct, Damasco)
walkDH = Walk(30, Damasco, Hills)
walkCI = Walk(6, Cathedral, Iglesia)
walkIH = Walk(20, Iglesia, Hills)
walkCP = Walk(7, Cathedral, Poke)
walkCA = Walk(11, Cathedral, Alcazar)
walkAH = Walk(20, Alcazar, Hills)

# Linking the graph through the adjacency lists of the locations

Plaza.adjacencylist = [walkPI, walkPC]
Irish.adjacencylist = [walkIA, walkIP]
Aqueduct.adjacencylist = [walkAB, walkAD]
Burbuja.adjacencylist = [walkBD]
Damasco.adjacencylist = [walkDH]
Cathedral.adjacencylist = [walkCI, walkCP, walkCA]
Poke.adjacencylist = [walkPIG, walkPA]
Iglesia.adjacencylist = [walkIH]
Alcazar.adjacencylist = [walkAH]

find_tour(3, Plaza, Hills)

# finally running the crucial function and checking that the output is correct, try changing the inputs to get your tour!