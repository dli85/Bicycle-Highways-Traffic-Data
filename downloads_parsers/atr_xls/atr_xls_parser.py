import xlrd
import re
import os
from pickle_utils import write_pickle_if_not_exists, read_pickle


# TODO: Add averages for duplicate streets?

downloads_dir = '../../downloads'
desired_keywords = "Type AUTOMATED TRAFFIC RECORDING"
desired_extension = ".xls"
parsed_files_path = "../parsed_files.pickle"
all_file_data = {}
all_file_data_file_path = 'atr_xls_data.pickle'
parsed_files = set()


def gen_list(directory=downloads_dir):
    result = []

    for x in os.walk(directory):
        for file_name in x[2]:
            if desired_keywords in file_name and desired_extension in file_name and ".xlsx" not in file_name:
                result.append(file_name)
        break

    return result


def parse_xls(xls_file_path):
    workbook = xlrd.open_workbook(xls_file_path)
    sheet = workbook.sheet_by_index(0)

    current_file_data = {}

    row_index = 0
    direction_type = sheet.row_values(row_index)[0]
    # print(direction_type)
    while "Location".lower() not in sheet.row_values(row_index)[0].lower():
        row_index += 1

    street_name = re.sub(r'\d', '', sheet.row_values(row_index)[0]).replace("Location", "").replace(":", "").strip()
    # print(street_name)

    while "Date".lower() not in sheet.row_values(row_index)[0].lower():
        row_index += 1
    row_index += 1

    all_rows_total = 0
    times_and_totals = []

    while '/' in sheet.row_values(row_index)[0] and row_index < sheet.nrows - 1 and len(sheet.row_values(row_index)) > 0:
        time = sheet.row_values(row_index)[1]
        total = sheet.row_values(row_index)[len(sheet.row_values(row_index)) - 1]
        row_index += 1
        all_rows_total += int(total)
        times_and_totals.append((time, total))
        # print(time + " " + str(total))

    current_file_data['direction_type'] = direction_type
    current_file_data['times_and_totals'] = times_and_totals
    current_file_data['total'] = all_rows_total

    if street_name in all_file_data:
        # print("DUPLICATE")
        pass

    all_file_data[street_name] = current_file_data


def read_parsed_files():
    global parsed_files
    try:
        parsed_files = read_pickle(parsed_files_path)
    except FileNotFoundError:
        pass


def update_pickle_file(file_path, data):
    try:
        os.remove(file_path)
        write_pickle_if_not_exists(file_path, data)
    except FileNotFoundError:
        write_pickle_if_not_exists(file_path, data)
    except PermissionError:
        print("Trying to delete parsed_files file to overwrite it, permission error")


if __name__ == '__main__':
    xls_list = gen_list()
    read_parsed_files()
    for path in xls_list:
        parse_xls(downloads_dir + "/" + path)
        parsed_files.add(path)
    update_pickle_file(parsed_files_path, parsed_files)
    update_pickle_file(all_file_data_file_path, all_file_data)



