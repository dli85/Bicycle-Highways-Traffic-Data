import xlrd
import os

downloads_dir = '../../downloads'
desired_keywords = "Type AUTOMATED TRAFFIC RECORDING"
desired_extension = ".xls"


def gen_list(directory=downloads_dir):
    result = []

    for x in os.walk(directory):
        for file_name in x[2]:
            if desired_keywords in file_name and desired_extension in file_name:
                print(file_name)
                result.append(downloads_dir + "/" + file_name)
        break

    return result


def parse_xls(xls_file_path):
    workbook = xlrd.open_workbook(xls_file_path)
    sheet = workbook.sheet_by_index(0)

    for i in range(sheet.nrows):
        print(sheet.row_values(i))
    input()


if __name__ == '__main__':
    xls_list = gen_list()

    for path in xls_list:
        parse_xls(path)
