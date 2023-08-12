import pandas as pd
from faker import Faker
fackers = Faker(locale='en_US')
df = pd.read_excel('Book1.xlsx', engine='openpyxl')
from csv2vcard import csv2vcard
aab = []
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
dd.to_csv('aaa.csv', index=False, header=True)
csv2vcard.csv2vcard('aaa.csv', ',')