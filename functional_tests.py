
from selenium import webdriver  # the web driver for functional tests

# local url of web app
localurl = 'http://127.0.0.1:8000'

# init browser
browser = webdriver.Firefox()  # use firefox for testing
browser.get(localurl)

# check if Django is there in the title
assert 'Django' in browser.title
