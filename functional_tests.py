"""
The functional tests / black box tests / acceptance tests / end2end tests
    for Skill List
        by Leon (Hao Wu)
"""
from selenium import webdriver  # the web driver for functional tests
import unittest  # use unittest module for whilte box tests
from selenium.webdriver.common.keys import Keys  # for sending key press to webdriver


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

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Arya Stark comes to the cool website that helps people saving their skills
        self.browser.get(URL_LOCAL)

        # She sees in the title, "Skill List", which is what the web app does.
        self.assertIn('Skill Tracker', self.browser.title)

        # She sees on the page, a big "Skill List" text showing
        header_text = self.browser.find_element_by_tag_name('h1').text  # find the first h1 el and get its text
        self.assertIn('Skill Tracker', header_text)

        # She's invited to enter a Skill Log immediately
        input_box = self.browser.find_element_by_id('id_new_item')  # find input box by id 'id_new_item'
        self.assertEqual(
            input_box.get_attribute('placeholder'),  # check to see if 'Enter a log' is the placeholder of the input box
            'Enter a log'
        )

        # She enters Poke the training dummy with needle, (Swordplay), needle is the name of her castle forged sword
        input_box.send_keys('Poke the training dummy with needle.')

        # When she press enter, the page updates, and lists "1. Poke the training dummy with needle."
        #   as an item to the skill log
        input_box.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')  # find the listing table by id
        rows = table.find_elements_by_tag_name('tr')  # get all table rows from table
        self.assertTrue(
            # see if any of the rows has the log, any(? x in []) is a little-known python built-in
            any(row.text == '1. Poke the training dummy with needle.' for row in rows)
        )

        # There's still a text box inviting her to add another log, she enters "chase the cat in the dungeon" (Sneaking)
        self.fail('listing first log finished, more to do...')

        # The page updates again, now showing two logs

        # She's satisfied and left.


"""main"""
if __name__ == '__main__':
    unittest.main()  # main runs the test runner which auto find all test_ functions and run them
