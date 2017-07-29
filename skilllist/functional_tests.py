"""
The functional tests / black box tests / acceptance tests / end2end tests
    for Skill List
        by Leon (Hao Wu)
"""
from selenium import webdriver  # the web driver for functional tests

"""conf"""

# local url of web app
localurl = 'http://127.0.0.1:8000'

# init browser
browser = webdriver.Firefox()  # use firefox for testing

""" user story """
# My lady comes to the cool website that helps people saving their skills
browser.get(localurl)

# She sees in the title, "Skill List", which is what the web app does.
assert 'Skill List' in browser.title

# She's satisfied and left.
browser.quit()
