from pokeapi import PokeAPI

PokeAPI = PokeAPI()

# desc: class for a pokemon
# constructor args: name - the name of the pokemon to create a class for
class Pokemon:
    def __init__(self, name=None):
        if name is None:
            self.name = ''
            self.number = 0
            self.type = []
            self.evolution = Evolution(chain=None)
            self.stats = BaseStats(stats=None)
        else:
            self.name = name

            # get pokemon number
            pokeNum = PokeAPI.GetPokeNum(name)
            if pokeNum != -1:
                self.number = pokeNum
            else:
                self.number = 0

            pokeType = PokeAPI.GetPokeType(name)
            # get pokemon type(s)
            if pokeType != -1:
                self.type = pokeType
            else:
                self.type = []

            # create a instance of the evolution
            evoChain = PokeAPI.GetEvoChain(name)
            if evoChain != -1:
                self.evolution = Evolution(evoChain)
            else:
                self.evolution = Evolution(chain=None)

            # create instance of stats
            baseStats = PokeAPI.GetBaseStats(name)
            if baseStats != -1:
                self.baseStats = BaseStats(baseStats)
            else:
                self.baseStats = BaseStats(stats=None)



# desc: class for pokemon evolution chain
# constructor args: chain - the chain field returned from the api
class Evolution:
    def __init__(self, chain=None):
        if chain is None:
            self.baseSpecies = {}
            self.evolutions = {}
        else:
            self.baseSpecies = chain['species']['name']

            # process the chain
            self.evolutions = {}
            for firstEvo in chain['evolves_to']:
                # get name and details of first level evo
                keyName = firstEvo['species']['name']
                firstVars = []
                for detailSet in firstEvo['evolution_details']:
                    firstVars.append(EvoDetails(detailSet))
                # append to evolutions dict
                self.evolutions[keyName] = firstVars

                if len(firstEvo['evolves_to']) > 0:
                    for secondEvo in firstEvo['evolves_to']:
                        # get names of second level evo
                        keyName = secondEvo['species']['name']
                        secondVars = []
                        for detailSet in secondEvo['evolution_details']:
                            secondVars.append(EvoDetails(detailSet))
                        # append to evolutions dict
                        self.evolutions[keyName] = secondVars

                        if len(secondEvo['evolves_to']) > 0:
                            for thirdEvo in secondEvo['evolves_to']:
                                # get names of third level evo
                                keyName = thirdEvo['species']['name']
                                thirdVars = []
                                for detailSet in thirdEvo['evolution_details']:
                                    thirdVars.append(EvoDetails(detailSet))
                                # append to evolutions dict
                                self.evolutions[keyName] = thirdVars



# desc: class for holding evolution details
# constructor args: details - a list containing the details for this evolution
class EvoDetails:
    def __init__(self, details):
        self.minLevel = details['min_level']
        self.minBeauty = details['min_beauty']
        self.timeOfDay = details['time_of_day']
        self.gender = details['gender']
        self.relPhyStats = details['relative_physical_stats']
        self.needsRain = details['needs_overworld_rain']
        self.upsideDown = details['turn_upside_down']
        self.item = details['item']
        self.trigger = details['trigger']
        self.knownMoveType = details['known_move_type']
        self.minAffection = details['min_affection']
        self.partyType = details['party_type']
        self.tradeSpecies = details['trade_species']
        self.partySpecies = details['party_species']
        self.minHappiness = details['min_happiness']
        self.heldItem = details['held_item']
        self.knownMove = details['known_move']
        self.location = details['location']



# desc: class for pokemon base stats
# constructor args: stats - a dictionary containing the stats for the pokemon
class BaseStats:
    def __init__(self, stats=None):
        if stats is None:
            self.hp = 0
            self.attack = 0
            self.defense = 0
            self.spAtk = 0
            self.spDef = 0
            self.speed = 0
        else:
            self.hp = stats['hp']
            self.attack = stats['attack']
            self.defense = stats['defense']
            self.spAtk = stats['special-attack']
            self.spDef = stats['special-defense']
            self.speed = stats['speed']
