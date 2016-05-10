import requests
from bs4 import BeautifulSoup
import re

import graph

url_subjects = 'http://www.uio.no/studier/emner/'
url_root = 'http://www.uio.no/'
print url_subjects
page_queue = []
work_queue = []
session = requests.session()

subjects = session.get(url_subjects)
soup = BeautifulSoup(subjects.text,'html.parser')

subject_graph = graph.Graph

for link in soup.find_all('h3'):
    print link
    if 'Andre emner' in link:
        continue
    link_res = re.search(r'"(\w.*?/)"',str(link))
    page_queue.append(url_subjects+link_res.group(0).replace('"',''))


print page_queue
for page in page_queue:
    print page
    for page_num in range(1,2):
        print 'Getting page {}'.format(page_num)
        subject_page = requests.get(page,params={'page':str(page_num)})
        temp_soup = BeautifulSoup(subject_page.text,'html.parser')
        check = temp_soup.find(id='vrtx-listing-filter-no-results')
        if check: #Breaks the loop
            print 'Last page reached. Continuing to next faculty'
            break
        else: #This is where is gather the subjects
            subjects = temp_soup.find_all(href=re.compile(r'/studier/emner/.*?/index.html'))
            for link in subjects:
                link_res = re.search(r'"(.*?)"', str(link)).group(0).replace('"','')
                #print url_root + link_res
                work_queue.append(url_root + link_res)

#vrtx-listing-filter-no-results

print 'Found %s subjects' % len(work_queue)

for course_site in work_queue:
    print "Parsing subject %s" % course_site
    temp_course = requests.get(course_site)
    soup = BeautifulSoup(temp_course.text, 'html.parser')

    pre_req = soup.find(id='prerequisites')

    name = soup.find(id='hdr')
    blurb = soup.find(id='course-content')

    print 'lol'



    print '\n' + '-'*20 + '\n'

