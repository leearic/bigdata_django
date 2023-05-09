import pandas as pd
import openpyxl
def do_data_diff(row_data_file, diff_data_file):
    row_data = pd.read_csv(row_data_file)
    diff_data = pd.read_csv(diff_data_file)

    row_data_ld = row_data['phone']
    diff_data_ld = diff_data['phone']

    row_data_set = set(row_data_ld.to_dict().values())
    diff_data_set = set(diff_data_ld.to_dict().values())

    diff_set = list(row_data_set - diff_data_set)

    df = pd.DataFrame(diff_set, columns=['phone'])
    df.to_excel('out.xlsx', index=False)


do_data_diff(row_data_file='./static/index/img/2023-05-09/716244b0-ee54-11ed-acfd-000c29c8d52d/aaaa.xlsx.csv', diff_data_file='/home/cc/PycharmProjects/bigdata_django/static/index/img/2023-05-09/716244b0-ee54-11ed-acfd-000c29c8d52d/bbbbbbbbb.xlsx.csv')
