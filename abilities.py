from pokeapi import PokeAPI
import requests

PokeAPI = PokeAPI()

class Abilities:
    def __init__(self):
        # initialize as blank
        self.abilityList = []
        self.abilities = []

    def GetAllAbilities(self):
        # get the list of abilities and their urls
        self.abilityList = PokeAPI.GetAbilityList()
        # get information for every ability
        for ability in self.abilityList:
            try:
                # get page with ability data
                response = requests.get(ability['url'])
                # try to raise exception
                response.raise_for_status()
                # convert to json and append to list
                abilityData = response.json()
                self.abilities.append(Ability(abilityData))
            except requests.exceptions.HTTPError as error:
                print('Error while getting ability data: %s' % error)



class Ability:
    def __init__(self, abilityData=None):
        if abilityData is None:
            self.name = None
            self.description = None
        else:
            self.name = None
            self.description = None
            # get english name of move
            for entry in abilityData['names']:
                if entry['language']['name'] == 'en':
                    self.name = entry['name']

            # get the effect description
            for entry in abilityData['effect_entries']:
                if entry['language']['name'] == 'en':
                    self.description = entry['effect']
