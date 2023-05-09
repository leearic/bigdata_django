from __future__ import absolute_import, unicode_literals
import json
import os

# import openpyxl
from bigdata_django.celery import app
from data_deduplication.models import Deduplication
from billiard.exceptions import Terminated
from django.conf import settings
import pandas as pd
import uuid
import datetime
class XLSXUTIL():
    def xlsx_to_csv(self, xlsx_file_path):
        try:
            data_xls = pd.read_excel(xlsx_file_path, index_col=0, engine='openpyxl')
            data_xls.to_csv(xlsx_file_path + '.csv', encoding='utf-8')
            return True
        except Exception as e:
            print(e)
            return False

    def do_data_diff(self, row_data_file_path, diff_data_file_path):
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d')

        general = uuid.uuid1()
        row_data = pd.read_csv(row_data_file_path)
        diff_data = pd.read_csv(diff_data_file_path)

        row_data_ld = row_data['phone']
        diff_data_ld = diff_data['phone']

        row_data_set = set(row_data_ld.to_dict().values())
        diff_data_set = set(diff_data_ld.to_dict().values())
        diff_set = list(diff_data_set -(row_data_set & diff_data_set))

        df = pd.DataFrame(diff_set, columns=['phone'])
        dirs = 'out/{0}/{1}'.format(nowtime, general)
        os.makedirs('static/data/' + dirs)
        outpath = dirs + '/out.xlsx'
        df.to_excel('static/data/' + outpath, index=False)
        return outpath

@app.task(throws=(Terminated),  soft_time_limit=120, time_limit=120)
def do_data_diff(data):
    data = json.loads(data)
    deduplication = Deduplication.objects.get(id=data[0]['pk'])
    if deduplication.task_done is True:
        return
    aa = XLSXUTIL()
    comparative_data = data[0]["fields"]["comparative_data"]
    raw_data = data[0]["fields"]["raw_data"]
    comparative_data_file_path = settings.MEIDABASEURL + comparative_data
    raw_data_file_path = settings.MEIDABASEURL + raw_data
    row_data_file_path = ''
    diff_data_file_path = ''
    for file_to_cover in [comparative_data_file_path, raw_data_file_path]:
        if aa.xlsx_to_csv(file_to_cover):
            row_data_file_path ='./' + raw_data_file_path+'.csv'
            diff_data_file_path = './' + comparative_data_file_path + '.csv'
            print('done ')

        else:
            print('error')
    outpath = ''
    try:
        outpath = aa.do_data_diff(row_data_file_path, diff_data_file_path)
        deduplication.status = True
        deduplication.out_data = outpath
    except Exception as e:
        deduplication.error = True
    deduplication.task_done =True
    deduplication.update_date = datetime.datetime.now()
    deduplication.save()



