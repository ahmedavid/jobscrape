import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

template = 'https://www.indeed.com/jobs?q={}&l={}'

def get_url(position, location):
  template = 'https://www.indeed.com/jobs?q={}&l={}'
  url = template.format(position, location)
  return url

def get_record(card):
  post_date = card.find('span', 'date')
  today = datetime.today().strftime('%Y-%m-%d')
  atag = card.h2.find('span',{"title":True})
  job_id =card.get("data-jk")
  print('===============================')
  print(job_id)
  job_title = atag.get("title")
  print(job_title)
  job_url = card.get('href')
  try:
      company_name = card.find('span','companyOverviewLink').a.text.strip()
  except AttributeError:
      company_name= card.find('span','companyName').text.strip()
  print(company_name)
  company_location = card.find('div','companyLocation').text.strip()
  one_response = requests.get('https://www.indeed.com' + job_url)
  one_soup = BeautifulSoup(one_response.text, 'html.parser')
  job_description = one_soup.find('div', {"id":"jobDescriptionText"})

  return (job_id,job_title,job_url,company_name,company_location,job_description)

def main(position, location):
  records = []
  url = get_url(position, location)
  pages = 0

  while(pages < 2):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('a','tapItem')
    for card in cards:
        record = get_record(card)
        records.append(record)
        
    try:
        next = soup.find('a', {'aria-label': 'Next'}).get('href')
        url = 'https://www.indeed.com' + next
        pages +=1
    except AttributeError:
        break
        
    print(len(records))
          
  with open('results.csv','a',newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    ## writer.writerow(["job_id","job_title","job_url","company_name","company_location","job_description"])
    writer.writerows(records)

main('machine learning engineer','new york ny')
main('software developer','new york ny')
main('front end developer','new york ny')