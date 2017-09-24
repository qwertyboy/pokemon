import requests

class PokeAPI:
    def __init__(self):
        # base api url
        self.baseUrl = 'http://pokeapi.co/api/v2/'


    # desc: function to get a list of urls and names for each pokemon
    # args: none
    # retn: a list of dicts containing the url and name of each pokemon on
    #       success or -1 on failure
    def GetPokeList(self):
        try:
            # starting url for the api
            startUrl = self.baseUrl + 'pokemon/'
            # get a response
            response = requests.get(startUrl)
            # raise an exception if we get an error
            response.raise_for_status()
            # convert to json, get next url and results
            json = response.json()
            nextUrl = json['next']
            pokeList = json['results']

            # get the rest of the pages until the end
            while nextUrl != None:
                response = requests.get(nextUrl)
                # convert to json, get next url and results
                json = response.json()
                nextUrl = json['next']
                results = json['results']
                for item in results:
                    pokeList.append(item)

            # return the completed list
            return pokeList
        except requests.exceptions.HTTPError as error:
            print('Error while getting Pokemon list: %s' % error)
            return -1


    # desc: function to get a list of urls and names for each pokemon species
    # args: none
    # retn: a list of dicts containing the url and name of each pokemon on
    #       success or -1 on failure
    def GetSpeciesList(self):
        try:
            # starting url for the api
            startUrl = self.baseUrl + 'pokemon-species/'
            # get a response
            response = requests.get(startUrl)
            # raise an exception if we get an error
            response.raise_for_status()
            # convert to json, get next url and results
            json = response.json()
            nextUrl = json['next']
            speciesList = json['results']

            # get the rest of the pages until the end
            while nextUrl != None:
                response = requests.get(nextUrl)
                # convert to json, get next url and results
                json = response.json()
                nextUrl = json['next']
                results = json['results']
                for item in results:
                    speciesList.append(item)

            # return the completed list
            return speciesList
        except requests.exceptions.HTTPError as error:
            print('Error while getting Species list: %s' % error)
            return -1


    # desc: function to get the types of a specific pokemon
    # args: pokemon - the pokemon name or id to get the types of
    # retn: a list of types or -1 on failure
    def GetPokeType(self, pokemon):
        url = self.baseUrl + 'pokemon/' + pokemon
        try:
            # get a response
            response = requests.get(url)
            # raise an exception if we get an error
            response.raise_for_status()
            # convert to json, get next url and results
            json = response.json()

            # get list of types
            types = json['types']
            foundTypes = []
            for item in types:
                foundTypes.append(item['type']['name'])

            return foundTypes
        except requests.exceptions.HTTPError as firstError:
            # handle the first error and retry using the pokemon's number
            print('Error while getting Pokemon types: %s' % firstError)
            print('Retrying with Pokemon number...')

            url = self.baseUrl + 'pokemon/' + str(self.GetPokeNum(pokemon))
            try:
                # get a response
                response = requests.get(url)
                # raise an exception if we get an error
                response.raise_for_status()
                # convert to json, get next url and results
                json = response.json()

                # get list of types
                types = json['types']
                foundTypes = []
                for item in types:
                    foundTypes.append(item['type']['name'])

                return foundTypes
            except requests.exceptions.HTTPError as secondError:
                print('Error while getting Pokemon types: %s' % secondError)
                return -1


    # desc: function to get the level a pokemon evolves at or the trigger
    # args: pokemon - the pokemon name or id to get the evolution stats for
    # retn: the chain data from the api or -1 on failure
    def GetEvoChain(self, pokemon):
        startUrl = self.baseUrl + 'pokemon-species/' + pokemon
        try:
            # get the species data
            speciesResp = requests.get(startUrl)
            # raise an exception if we get an error
            speciesResp.raise_for_status()
            speciesJson = speciesResp.json()
            multiForm = len(speciesJson['varieties']) > 1

            # get the evolution chain data
            evoUrl = speciesJson['evolution_chain']['url']
            evoResp = requests.get(evoUrl)
            # raise an exception if we get an error
            evoResp.raise_for_status()
            evoJson = evoResp.json()

            # return the chain
            return evoJson['chain']
        except requests.exceptions.HTTPError as error:
            print('Error while getting Pokemon types: %s' % error)
            return -1


    # desc: function to get the base stats of a pokemon
    # args: pokemon - the pokemon name or id to get the stats for
    # retn: a dictionary with the base stats or -1 on failure
    def GetBaseStats(self, pokemon):
        stats = {'hp': 0, 'attack': 0, 'defense': 0, 'special-attack': 0, 'special-defense': 0, 'speed': 0}
        startUrl = self.baseUrl + 'pokemon/' + pokemon
        try:
            # get the pokemon information
            response = requests.get(startUrl)
            # raise an exception if we get an error
            response.raise_for_status()

            json = response.json()
            for stat in json['stats']:
                statName = stat['stat']['name']
                stats[statName] = stat['base_stat']

            return stats
        except requests.exceptions.HTTPError as firstError:
            print('Error while getting Pokemon base stats: %s' % firstError)
            print('Retrying with Pokemon number...')

            startUrl = self.baseUrl + 'pokemon/' + str(self.GetPokeNum(pokemon))
            try:
                # get the pokemon information
                response = requests.get(startUrl)
                # raise an exception if we get an error
                response.raise_for_status()

                json = response.json()
                for stat in json['stats']:
                    statName = stat['stat']['name']
                    stats[statName] = stat['base_stat']

                return stats
            except requests.exceptions.HTTPError as secondError:
                print('Error while getting Pokemon base stats: %s' % secondError)
                return -1


    # desc: function to get the number of a pokemon
    # args: pokemon - the pokemon to get number of
    # retn: the number of the pokemon or -1 if not found
    def GetPokeNum(self, pokemon):
        startUrl = self.baseUrl + 'pokemon-species/' + pokemon
        try:
            # get pokemon information
            response = requests.get(startUrl)
            # raise an exception if we get an error
            response.raise_for_status()
            json = response.json()
            dexNumbers = json['pokedex_numbers']
            for entry in dexNumbers:
                # get entry name
                entryName = entry['pokedex']['name']
                # get national number
                if entryName == 'national':
                    return entry['entry_number']
            return -1
        except requests.exceptions.HTTPError as error:
            print('Error while getting Pokemon number: %s' % error)
            return -1


    # desc: function to get a list of move entries
    # args: none
    # retn: a list of dictionaries with a url and name for each move
    def GetMoveList(self):
        startUrl = self.baseUrl + 'move/'
        moveList = []
        try:
            # get initial response to get number of moves
            response = requests.get(startUrl)
            urlLimit = response.json()['count']
            # get full results page and json-ify it
            limitUrl = startUrl + '?limit=' + str(urlLimit)
            response = requests.get(limitUrl)
            json = response.json()
            # store results into list
            for move in json['results']:
                moveList.append(move)
            return moveList
        except requests.exceptions.HTTPError as error:
            print('Error while getting moves: %s' % error)
            return -1
