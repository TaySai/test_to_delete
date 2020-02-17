import requests as rq
from bs4 import BeautifulSoup as bs
import csv
import os
import pandas as pd
import unidecode


# def create_folder(path):
#     try:
#         os.mkdir(path)
#     except OSError:
#         print ("Creation of the directory %s failed" % path)
#     else:
#         print ("Successfully created the directory %s " % path)



# def download_map_galaxy(name, path, url):
#     name = name.lower().replace(' ', '-')
#     extension = url.split("/")[-1].split('.')[-1]
#     r = rq.get('http://messier.obspm.fr/' + url, timeout=0.5)
#
#     if r.status_code == 200:
#         with open(path+name+'.'+extension, 'wb') as f:
#             f.write(r.content)

path = "./maps/"
create_folder(path)

def create_csv_data():
    r = rq.get('http://messier.obspm.fr/CONindex2_f.html')

    soup = bs(r.content, 'html.parser')

    data = []

    fieldnames = ['messier_name', 'messier_link', 'messier_surname', 'messier_form', 'galaxy_name', 'galaxy_link',
                  'galaxy_map_link']

    for x in soup.ul.find_all('li', recursive=False):
        row = dict()
        row['galaxy_name'] = unidecode_word(x.i.a.get_text().strip())
        row['galaxy_link'] = 'http://messier.obspm.fr/' + x.i.a['href']

        r_galaxy = rq.get(row['galaxy_link'])
        soup_galaxy = bs(r_galaxy.content, 'html.parser')

        download_map_galaxy(row['galaxy_name'], path, soup_galaxy.img['src'])

        row['galaxy_map_link'] = 'http://messier.obspm.fr/' + soup_galaxy.img['src']

        for y in x.ul.find_all('li'):
            messier = dict()
            try:
                surname = ' '.join(y.b.get_text().split())
            except AttributeError:
                surname = ''

            messier['messier_name'] = unidecode_word(y.a.get_text().strip())
            messier['messier_link'] = 'http://messier.obspm.fr/' + y.a['href']
            messier['messier_surname'] = unidecode_word(surname.replace(',', ''))
            messier['messier_form'] = unidecode_word(
                ' '.join(list(filter(None, [x.strip() for x in y(recursive=False, text=True)]))))

            r_messier = rq.get(messier['messier_link'])

            soup_messier = bs(r_messier.content, 'html.parser')

            try:
                for x, y in zip(soup_messier.table.find_all('th'), soup_messier.table.find_all('td')):
                    name = unidecode_word(x.get_text())
                    name = name.strip().lower().replace(' ', '_')
                    if name not in fieldnames:
                        fieldnames.append(name)
                    messier[name] = y.get_text().split('(')[0].strip()
            except AttributeError:
                pass

            messier.update(row)

            data.append(messier)

    with open("data.csv","w",newline="") as file_writer:
        fields = fieldnames
        writer=csv.DictWriter(file_writer,fieldnames=fields)
        writer.writeheader()
        for x in data:
            writer.writerow(x)