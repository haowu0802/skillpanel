"""
The functional tests / black box tests / acceptance tests / end2end tests
    for Skill List
        by Leon (Hao Wu)
"""
from django.test import LiveServerTestCase
from selenium import webdriver  # the web driver for functional tests
from selenium.webdriver.common.keys import Keys  # for sending key press to webdriver
from selenium.common.exceptions import WebDriverException
import time  # to use sleep


"""conf"""
URL_LOCAL = 'http://127.0.0.1:8000'  # local url of web app
WAIT_SEC = 3  # number of seconds wait at start
SHORT_PAUSE = 0.5  # generic short wait, for latency, slow machines
LONG_PAUSE = 10  # generic long pause, for debugging
MAX_WAIT = 10  # wait no longer than this


class NewVisitorTest(LiveServerTestCase):  # group tests into classes
    """a new visitor's common behavior first time to the web app"""
    def setUp(self):
        """setUp runs before each test"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(WAIT_SEC)

    def tearDown(self):
        """tearDown runs after each test, even with exceptions"""
        self.browser.quit()

    def wait_for_text_in_rows_of_table(self, row_text):
        """
        wait for table to load and check for existence of row_text in table
            SHORT_PAUSE between reties
        :param row_text:
        :return:
        """
        start_time = time.time()  # timer for MAX WAIT
        while True:
            try:
                table = self.browser.find_element_by_id('id_log_table')  # find the logs table by id
                rows = table.find_elements_by_tag_name('tr')  # get all table rows from table
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(SHORT_PAUSE)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Arya Stark comes to the cool website that helps people saving their skills
        self.browser.get(self.live_server_url)

        # She sees in the title, "Skill List", which is what the web app does.
        self.assertIn('Skill Tracker', self.browser.title)

        # She sees on the page, a big "Skill List" text showing
        header_text = self.browser.find_element_by_tag_name('h1').text  # find the first h1 el and get its text
        self.assertIn('Skill Logs', header_text)

        # She's invited to enter a Skill Log immediately
        input_box = self.browser.find_element_by_id('id_new_log')  # find input box by id 'id_new_item'
        self.assertEqual(
            input_box.get_attribute('placeholder'),  # check to see if 'Enter a log' is the placeholder of the input box
            'Enter a log'
        )

        # She enters Poke the training dummy with needle, (Swordplay), needle is the name of her castle forged sword
        input_box.send_keys('Poke the training dummy with needle.')

        # When she press enter, the page updates, and lists "1. Poke the training dummy with needle."
        #   as an item to the skill log
        input_box.send_keys(Keys.ENTER)
        self.wait_for_text_in_rows_of_table('1. Poke the training dummy with needle.')

        # There's still a text box inviting her to add another log, she enters "Chase the cat in the dungeon" (Sneaking)
        input_box = self.browser.find_element_by_id('id_new_log')  # re-assign the new input box to input_box
        input_box.send_keys('Chase the cat in the dungeon.')  # a different log
        input_box.send_keys(Keys.ENTER)

        # The page updates again, now showing two logs
        self.wait_for_text_in_rows_of_table('1. Poke the training dummy with needle.')
        self.wait_for_text_in_rows_of_table('2. Chase the cat in the dungeon.')

        # Arya wonders if the site will remember her lists, and sees that a URL is generated, with some text
        self.fail('listing first log finished, more to do...')

        # She visits the URL, and the logs are still there

        # She's satisfied and left.

