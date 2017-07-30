"""
The functional tests / black box tests / acceptance tests / end2end tests
    for Skill List
        by Leon (Hao Wu)
"""
from selenium import webdriver  # the web driver for functional tests
import unittest  # use unittest module for whilte box tests


"""conf"""
URL_LOCAL = 'http://127.0.0.1:8000'  # local url of web app
WAIT_SEC = 3  # number of seconds wait at start


class NewVisitorTest(unittest.TestCase):  # group tests into classes
    """a new visitor's common behavior first time to the web app"""
    def setUp(self):
        """setUp runs before each test"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(WAIT_SEC)

    def tearDown(self):
        """tearDown runs after each test, even with exceptions"""
        self.browser.quit()

    def test_can_visit_the_page_and_leave(self):
        # My lady comes to the cool website that helps people saving their skills
        self.browser.get(URL_LOCAL)
        # She sees in the title, "Skill List", which is what the web app does.
        self.assertIn('Skill Tracker', self.browser.title)
        self.fail('todo')
        # She's satisfied and left.


"""main"""
if __name__ == '__main__':
    unittest.main()  # main runs the test runner which auto find all test_ functions and run them
