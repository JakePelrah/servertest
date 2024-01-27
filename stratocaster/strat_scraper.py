import requests
from bs4 import BeautifulSoup
import csv
import os
import threading
import boto3
import csv

    
outfile = open('fender-stratocaster_index.csv', 'a')
indexwriter = csv.writer(outfile, delimiter=',')

session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id='DO00NMERU2TN2VAJY37W',
                        aws_secret_access_key='BautF79hHbv5tJMgmVpzszdY/wRu/kXMSlwlWibRyHQ')


def make_request(row):
    url = row[5]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', {"class": "lightbox-image-item"})
   
    for item in items:
        img_url = item.find('img')['src'].split('t_card-square')[-1]
        try:
            new_url = 'https://rvb-img.reverb.com/image/upload/' + img_url
            thread = threading.Thread(target=download_image, args=(
                    row,), kwargs={'img_url': img_url, 'new_url': new_url})
            thread.start()
            thread.join()
        except:
            print(img_url)
    


def download_image(row, new_url, img_url):
    r = requests.get(new_url)
    if r.status_code == 200:
        try:     
            client.get_object(Bucket='egil-ic', Key='fender-stratocaster/' + img_url.split('/')[-1])
            print('file exists') 
            indexwriter.writerow(['fender-stratocaster', row[2] + '_' + row[1] +'_'+ img_url.split('/')[-1]])
        except:
            client.put_object(Body=r.content, Bucket='egil-ic', Key='fender-stratocaster/' + img_url.split('/')[-1])
            indexwriter.writerow(['fender-stratocaster', row[2] + '_' + row[1] +'_'+ img_url.split('/')[-1]])
    outfile.flush()
           
      
    

# Open file
i=0
with open('stratocaster.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        print(i)
        thread = threading.Thread(target=make_request, args=(row,))
        thread.start()
        thread.join()
        i+=1
