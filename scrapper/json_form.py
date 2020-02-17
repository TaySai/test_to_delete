import requests as rq
from bs4 import BeautifulSoup as bs
import json

def create_json_data():
    r = rq.get('http://messier.obspm.fr/CONindex2_f.html')

    soup = bs(r.content, 'html.parser')

    data = {'galaxies': []}

    for x in soup.ul.find_all('li', recursive=False):
        row = dict()
        row['galaxy_name'] = x.i.a.get_text().strip()
        row['galaxy_link'] = 'http://messier.obspm.fr/' + x.i.a['href']

        row['messiers'] = []
        for y in x.ul.find_all('li'):

            try:
                surname = ' '.join(y.b.get_text().split())
            except AttributeError:
                surname = ''

            row['messiers'].append(
                {
                    'messier_name': y.a.get_text().strip(),
                    'messier_link': 'http://messier.obspm.fr/' + y.a['href'],
                    'messier_surname': surname.replace(',', ''),
                    'messier_form': ' '.join(list(filter(None, [x.strip() for x in y(recursive=False, text=True)])))
                }
            )
        data['galaxies'].append(row)

    with open('galaxies.json', 'w') as outfile:
        json.dump(data, outfile)