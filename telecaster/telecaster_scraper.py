import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil

def make_request(url):
    response = requests.get(url)
    return response.text


def make_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


# Open file
with open('fender_telecaster.csv') as file_obj:

    # Create reader object by passing the file
    # object to reader method
    reader_obj = csv.reader(file_obj)

    # Iterate over each row in the csv
    # file using reader object
    i=0
    for row in reader_obj:
        url = row[5]
        folder = 'images/' + row[2] + '-' + row[1]
        # if folder does not exist, create it and download images
        try:
            os.makedirs(folder, exist_ok=False)
            html = make_request(row[5])
            soup = make_soup(html)
            items = soup.find_all('div', {"class": "lightbox-image-item"})
            for item in items:
                img_url = item.find('img')['src'].split('t_card-square')[-1]
                try:
                    new_url = 'https://rvb-img.reverb.com/image/upload/' + img_url
                    r = requests.get(new_url, stream=True)
                    if r.status_code == 200:
                        filename = folder + '/' + img_url.split('/')[-1]
                        print(filename)
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        with open(filename, 'wb') as f:
                            for chunk in r:
                                f.write(chunk)
                        shutil.copy(filename, 'telecaster_merged/' + img_url.split('/')[-1])
                        
                except:
                    print(img_url)
        except:
            print('folder exists',folder)
    
    

