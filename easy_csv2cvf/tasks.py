from __future__ import absolute_import, unicode_literals
import json
from bigdata_django.celery import app

from billiard.exceptions import Terminated

from loguru import logger

from .models import CsvFiles
import pandas as pd
from faker import Faker
fackers = Faker(locale='en_US')

from csv2vcard import csv2vcard
from csv2vcard.parse_csv import parse_csv
from csv2vcard.create_vcard import create_vcard
# from csv2vcard.export_vcard import export_vcard
import os


def acsv2vcard(csv_filename: str, csv_delimeter: str, path: str):
    """
    Main function
    """
    if not os.path.exists(path):
        print("Creating /export folder...")
        os.makedirs(path)
    logger.info(path)

    for c in parse_csv(csv_filename, csv_delimeter):
        vcard = create_vcard(c)
        try:
            with open(path + "/" + vcard['filename'], "w") as f:
                f.write(vcard['output'])
                f.close()
                print(f"Created vCard 3.0 for {vcard['name']}.")
        except IOError:
            print(f"I/O error for {vcard['filename']}")

@app.task(throws=(Terminated),  soft_time_limit=240, time_limit=240)
def do_data_diff(data):
    aab = []
    logger.info(data)
    data = json.loads(data)
    csvmodel = CsvFiles.objects.get(id=data[0]["pk"])
    out_file_path = './static/data/' + str(csvmodel.raw_data) + '.csv'
    logger.info(csvmodel.task_name)
    logger.info('hello world')
    df = pd.read_excel(csvmodel.raw_data, engine='openpyxl')


    for row in df.index.values:
        aa = {}
        aa['last_name'] = fackers.first_name()
        aa['first_name'] = fackers.last_name()
        aa['org'] = fackers.company()
        aa['title'] = fackers.job()
        aa['phone'] = df.iloc[row, 0]
        aa['email'] = fackers.email()
        aa['website'] = fackers.url()
        aa['street'] = fackers.address()
        aa['city'] = fackers.city_suffix()
        aa['p_code'] = fackers.postcode()
        aa['country'] = fackers.country()
        print(df.iloc[row, 0])
        aab.append(aa)
    dd = pd.DataFrame.from_dict(aab)
    dd.to_csv(out_file_path, index=False, header=True)
    acsv2vcard(out_file_path, ',', out_file_path.split('.xlsx.csv')[0])
    out_path = (out_file_path.split('.xlsx.csv')[0] + '/../all.vcf').split('/static/data/')[1]
    logger.info(out_path)
    cmd = 'cat ' + out_file_path.split('.xlsx.csv')[0] + '/*.vcf > ' + out_file_path.split('.xlsx.csv')[0] + '/../all.vcf'
    logger.info(cmd)

    os.system(cmd)
    csvmodel.out_data = '/' + out_path
    csvmodel.save()


