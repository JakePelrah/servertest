import requests
from bs4 import BeautifulSoup
import csv
import os
import csv
import concurrent.futures


outfile = open('sg_images.csv', 'w')
indexwriter = csv.writer(outfile, delimiter=',')



def get_image_urls(row):
    url = row[4]
    print(row)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', {"class": "lightbox-image-item"}) 
    for item in items:
        img_url = item.find('img')['src'].split('t_card-square')[-1]
        full_url = 'https://rvb-img.reverb.com/image/upload/' + img_url
        # image name, image url, full url
        indexwriter.writerow([row[0] + '_' + row[1] +'_'+ img_url.split('/')[-1], full_url])
        outfile.flush()
        if not os.path.exists('images/' + row[0] + '_' + row[1] +'_'+ img_url.split('/')[-1]):                
            response = requests.get(full_url)
            with open('images/' + row[0] + '_' + row[1] +'_'+ img_url.split('/')[-1], 'wb') as f:
                f.write(response.content)
        else:
            print('Image already exists')
    


with open('sg_listings.csv') as file_obj:
    listings = list(csv.reader(file_obj))
    
    # Use a ThreadPoolExecutor to download images in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_image_urls, listings)
       

