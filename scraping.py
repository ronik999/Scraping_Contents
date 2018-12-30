from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import lxml.html as lh
import pandas as pd
import csv
import numpy as np

csv_file=open('scraping.csv','w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Restaurant Name','Address','Description','Ratings','Other Details'])

page_no=0
for page_no in range(1,700):

    try:
        page=requests.get('http://v1.foodmandu.com/RestaurantDetail.aspx?RestaurantID='+str(page_no))
        soup = BeautifulSoup(page.text, 'html.parser')
        body=soup.find('div',class_='master-wrapper-content')
        #restaurant_name
        rest_name=body.find('h1',class_='restReviewName')
        name=rest_name.text

        #address
        rest_address=body.find('h2',class_='restaddressReview')
        address=rest_address.text

        #description
        desc=body.find('span',class_='descText')
        description=desc.text

        #ratings
        rate=body.find('span', attrs={'id': 'ctl00_ctl00_cph1_cph1_as1_RestaurantRating2_lblRatingAverage'})
        ratings=rate.text

        #other details
        other_details=body.find('table', attrs={'class': 'box-table'})

        detail=[]
        for i in other_details.find_all("tr"):
            result = ""
            for j in i.find_all("td"): # find the cell tags
                result += j.text + " "
        

            detailed=result.rstrip(' ')
            detail.append(detailed)
   
        #converting row to column
        detail_row=np.array(detail)
        detail_column=np.reshape(detail_row,(6,1))
        details=str(detail_column)[1:-1]
        print(page_no)
        page_no=page_no+1
    
        
    
        csv_writer.writerow([name,address,description,ratings,details])
    except:
        continue
csv_file.close()


