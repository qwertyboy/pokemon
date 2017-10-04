from abilities import Abilities
import csv

# create instance
abilities = Abilities()

print('Querying API for ability information...')
abilities.GetAllAbilities()
print('Finished getting ability information')


print('Writing file...')
with open('databases/ability_database.csv', 'w', newline='') as abilityDB:
    writer = csv.writer(abilityDB, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    headers = ['Name', 'Description']
    writer.writerow(headers)

    for ability in abilities.abilities:
        # get each piece of information
        name = ability.name
        description = ability.description
        # contrsuct the row
        row = [name, description]
        # write the row
        writer.writerow(row)

print('Finished!')
