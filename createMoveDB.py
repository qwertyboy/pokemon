from moves import Moves
import csv
import time

print('Querying API for move information...')
moves = Moves()
print('Finished getting move information')


print('Writing file...')
with open('move_database.csv', 'w', newline='') as moveDB:
    writer = csv.writer(moveDB, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    headers = ['Name', 'Description', 'Type', 'Category', 'Power', 'Accuracy', 'PP']
    writer.writerow(headers)

    for move in moves.moves:
        # get each piece of information
        name = move.name
        description = move.description
        moveType = move.type
        category = move.category
        power = move.power
        accuracy = move.accuracy
        pp = move.pp
        # contrsuct the row
        row = [name, description, moveType, category, power, accuracy, pp]
        # write the row
        writer.writerow(row)

print('Finished!')
