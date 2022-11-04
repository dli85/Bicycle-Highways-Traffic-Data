import csv

# Reads the search results csv and returns a list of file names
def read_csv(filename, startingrow):
    result = []
    start = startingrow

    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        line_number = 0
        for row in reader:
            if line_number > start:
                original_file = row[6]
                split = original_file.split(" ")
                result.append(original_file)
            line_number += 1

    return result