'''Assignment Test File'''
import csv

import pytest
import assignment

zen=assignment.ZenPortal()

@pytest.mark.first_scenario
def test_login():
    '''Test login '''
    assert assignment.ZenPortal.login(zen) == "https://www.zenclass.in/class"

@pytest.mark.second_scenario
def test_menuitems():
    '''Test Menu Items'''
    assert assignment.ZenPortal.list_elements(zen) == \
    ['Class', 'Dashboard', 'Tasks', 'Hackathon',
     'Capstone', 'Queries', 'Requirements', 'Applications',
     'Interviewtasks', 'Leave-applications',
     'Mock-interview', 'Certificate']

@pytest.mark.third_scenario
def test_rasiequeries():
    '''Test queries'''
    assert assignment.ZenPortal.raise_queries(zen)

@pytest.mark.fourth_scenario
def test_wescraping():
    '''Test scrapping'''
    with open("scrappdata.csv",'w') as csvfile:
        csvwritter= csv.writer(csvfile)
        csvwritter.writerow(assignment.ZenPortal().scrap_data())

@pytest.mark.fifth_scenario
def test_closebrowser():
    '''Test closebrowser'''
    assignment.ZenPortal.close_browser(zen)
