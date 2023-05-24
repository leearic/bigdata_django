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
            data_xls.to_csv('./static/data/' + str(xlsx_file_path) + '.csv')
            return True
        except Exception as e:
            print(e)
            return False

    def do_data_diff(self, row_data_file_path_list, diff_data_file_path_list):
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d')

        general = uuid.uuid1()
        aa = []
        for i in row_data_file_path_list:
            abc = pd.read_csv(i + '.csv')
            aa.append(abc)
        row_data = pd.concat(aa)

        aa = []
        for i in diff_data_file_path_list:
            abc = pd.read_csv(i + '.csv')
            aa.append(abc)
        diff_data = pd.concat(aa)
        row_data_ld = row_data['phone']
        diff_data_ld = diff_data['phone']


        row_data_set = set(row_data_ld.to_dict().values())
        diff_data_set = set(diff_data_ld.to_dict().values())
        diff_set = list(diff_data_set - (row_data_set & diff_data_set))
        #
        df = pd.DataFrame(diff_set, columns=['phone'])
        dirs = 'out/{0}/{1}'.format(nowtime, general)
        os.makedirs('static/data/' + dirs)
        outpath = dirs + '/out.csv'
        df.to_csv('static/data/' + outpath, header=True, index=False, encoding='utf-8')
        return outpath

@app.task(throws=(Terminated),  soft_time_limit=240, time_limit=240)
def do_data_diff(data):
    aa = XLSXUTIL()
    data = json.loads(data)

    deduplication = Deduplication.objects.get(id=data[0]['pk'])

    if deduplication.task_done is True:
        return
    try:
        origdata_data_path_list = []
        for i in deduplication.origdata.all():
            origdata_data_path = settings.MEIDABASEURL + str(i.raw_data)
            aa.xlsx_to_csv(origdata_data_path)
            origdata_data_path_list.append(origdata_data_path)

        comparative_data_path_list = []
        for i in deduplication.DiffData.all():
            comparative_data_path = settings.MEIDABASEURL + str(i.comparative_data)
            comparative_data_path_list.append(comparative_data_path)
            aa.xlsx_to_csv(comparative_data_path)

        outpath = ''
        outpath = aa.do_data_diff(origdata_data_path_list, comparative_data_path_list)
        deduplication.status = True
        deduplication.out_data = outpath

    except Exception as e:
        deduplication.errorlog = e
        deduplication.error = True
    deduplication.task_done = True
    deduplication.update_date = datetime.datetime.now()
    deduplication.save()



