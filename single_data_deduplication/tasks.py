from __future__ import absolute_import, unicode_literals
import json
import os

# import openpyxl
from bigdata_django.celery import app
from single_data_deduplication.models import Deduplication
from billiard.exceptions import Terminated
# from django.conf import settings
import pandas as pd
import uuid
from loguru import logger
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

    def do_data_diff(self, deduplication):
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d')

        general = uuid.uuid1()
        origdatalist = []
        for i in deduplication.origdata.all():
            origdatalist.append(i.name)
        diffdatalist = []
        for i in deduplication.DiffData.all():
            diffdatalist.append(i.name)

        row_data = pd.read_csv('./static/data/' + str(deduplication.raw_data) + '.csv')

        origdatalist_values = []
        for i in origdatalist:
            origdatalist_values = origdatalist_values + row_data[i].drop_duplicates().values.tolist()
        origdatalist_values = set(origdatalist_values)


        diffdatalist_values = []
        for ii in diffdatalist:
            diffdatalist_values = diffdatalist_values + row_data[ii].drop_duplicates().values.tolist()
        diffdatalist_values = set(diffdatalist_values)

        diff_set = list(set(diffdatalist_values - (origdatalist_values & diffdatalist_values)))

        # #
        df = pd.DataFrame(diff_set, columns=['Diff'])
        dirs = 'out/{0}/{1}'.format(nowtime, general)
        os.makedirs('static/data/' + dirs)
        outpath = dirs + '/diff.csv'
        df.to_csv('static/data/' + outpath, header=True, index=False, encoding='utf-8')
        return outpath

@app.task(throws=(Terminated),  soft_time_limit=240, time_limit=240)
def do_single_data_diff(data):
    aa = XLSXUTIL()
    data = json.loads(data)

    for ii in data:
        logger.info('current id is: ' + str(ii))
        deduplication = Deduplication.objects.get(id=ii['pk'])
        if deduplication.task_done is True:
            continue
        try:
            # cover xmls to csv
            aa.xlsx_to_csv(deduplication.raw_data)
            outpath = ''
            outpath = aa.do_data_diff(deduplication)
            deduplication.status = True
            deduplication.out_data = outpath

        except Exception as e:
            deduplication.errorlog = e
            deduplication.error = True
        deduplication.task_done = True
        deduplication.update_date = datetime.datetime.now()
        deduplication.save()
        #

