import csv

# Reads the search results csv and returns a list of file names
def read_csv(filename):
    result = []

    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        line_number = 0
        for row in reader:
            if line_number != 0:
                original_file = row[6]
                split = original_file.split(" ")
                result.append(original_file)
            line_number += 1

    return result