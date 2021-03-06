#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

import graph

import pickle

url_subjects = 'http://www.uio.no/studier/emner/'
url_root = 'http://www.uio.no/'
print url_subjects
page_queue = []
work_queue = []
session = requests.session()

subjects = session.get(url_subjects)
soup = BeautifulSoup(subjects.text,'html.parser')

subject_graph = graph.Graph()

def main():
    get_faculty()
    print page_queue
    get_subjects()
    parse_course_sites()
    build_dependencies()

    output = open('subject_graph.dat', 'wb')

    # Pickle dictionary using protocol 0.
    pickle.dump(subject_graph, output)

    return 0


def get_faculty():

    for link in soup.find_all('h3'):
        print link
        if 'Andre emner' in link:
            continue
        link_res = re.search(r'"(\w.*?/)"',str(link))
        page_queue.append(url_subjects+link_res.group(0).replace('"',''))


def get_subjects():
    for page in page_queue:
        print page
        for page_num in range(1,200):
            print 'Getting page {}'.format(page_num)
            subject_page = requests.get(page,params={'page':str(page_num)})
            temp_soup = BeautifulSoup(subject_page.text.encode('utf-8'),'html.parser')
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


def parse_course_sites():

    for course_site in work_queue:

        if not 'INF' in course_site:
            continue
        #print "Parsing subject %s" % course_site
        temp_course = requests.get(course_site)
        soup = BeautifulSoup(temp_course.text, 'html.parser')

        pre_req = soup.find(id='prerequisites')
        if pre_req is not None:
            if pre_req.findChild('ul'):
                pre_req = pre_req.findChild('ul').text.encode('utf-8')
                #print "Pre req: {}".format(pre_req)
            elif pre_req.findChild('p'):
                pre_req = pre_req.findChild('p').text.encode('utf-8')
                #print "Pre req: {}".format(pre_req)


        name = soup.find(id='vrtx-course-title-toc')

        name = name.findChild('h1')
        code = name.text.encode('utf-8')

        p = re.compile(ur'([A-Z0-9-]{4,})', re.UNICODE)
        code = p.findall(code)[0]


        print code

        blurb = soup.find(id='course-content')
        if blurb:
            blurb = blurb.findChild('p')

        node = graph.Node(code=code,name=name.text.encode('utf-8'),pre_req=pre_req,site=course_site)
        subject_graph.add_node(node)

        #print '\n' + '-'*20 + '\n'

def build_dependencies():

    for sub_value in subject_graph.get_graph().keys():
        subjects = subject_graph.get_graph().get(sub_value)
        pre_req = parse_pre_req(subjects)
        for req_subs in pre_req:
            req_node = subject_graph.get_node(req_subs)
            if req_node is None:
                print 'Can not find {0}'.format(req_subs)
                continue
            subjects.add_related_node(req_node)

        subjects.state(out=True)


def parse_pre_req(subject):
    results = []
    p = re.compile(ur'([A-Z0-9]{4,})',re.UNICODE)
    text = subject.get_pre_req()
    if text:
        results = p.findall(str(text))

    return results

main()