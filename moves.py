from pokeapi import PokeAPI
import requests

PokeAPI = PokeAPI()

# desc: class containing moves
# constructor args: none
class Moves:
    def __init__(self):
        # initialize as blank
        self.moveList = []
        self.moves = []

    def GetAllMoves(self):
        # get the list of moves and their urls
        self.moveList = PokeAPI.GetMoveList()
        # get information for every move
        for move in self.moveList:
            try:
                # get page with move data
                response = requests.get(move['url'])
                # try to raise exception
                response.raise_for_status()
                # convert to json and append to list
                moveData = response.json()
                self.moves.append(Move(moveData))
            except requests.exceptions.HTTPError as error:
                print('Error while getting move data: %s' % error)



# name, pp, type, category, power, acc, desc
class Move:
    def __init__(self, moveData=None):
        if moveData is None:
            self.name = None
            self.description = None
            self.pp = None
            self.type = None
            self.category = None
            self.power = None
            self.accuracy = None
        else:
            # get english name of move
            for entry in moveData['names']:
                if entry['language']['name'] == 'en':
                    self.name = entry['name']

            # get description of move
            effectChance = str(moveData['effect_chance'])
            for entry in moveData['effect_entries']:
                if entry['language']['name'] == 'en':
                    desc = entry['short_effect']
                    self.description = desc.replace('$effect_chance', effectChance)

            # get pp
            self.pp = moveData['pp']
            # get type
            self.type = moveData['type']['name']
            # get category
            self.category = moveData['damage_class']['name']
            # get power
            self.power = moveData['power']
            # get accuracy
            self.accuracy = moveData['accuracy']
