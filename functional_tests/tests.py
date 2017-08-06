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
        """HELPER:
        setUp runs before each test"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(WAIT_SEC)

    def tearDown(self):
        """HELPER:
        tearDown runs after each test, even with exceptions"""
        self.browser.quit()

    def wait_for_text_in_rows_of_table(self, row_text):
        """HELPER
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

    def test_can_start_a_list_for_one_user(self):
        """FT-CHECK: a user can start a new Tracker by adding a Log"""
        # Arya Stark comes to the cool website that helps people saving their skills
        self.browser.get(self.live_server_url)

        # She sees in the title, "Skill List", which is what the web app does.
        self.assertIn('Skill Tracker', self.browser.title)

        # She sees on the page, a big "Skill List" text showing
        header_text = self.browser.find_element_by_tag_name('h1').text  # find the first h1 el and get its text
        self.assertIn('Skill Tracker', header_text)

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

        # Arya wonders if the site will remember her trackers, and sees that a URL is generated, with some text

        # She visits the URL, and the logs are still there

        # She's satisfied and left.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """FT-CHECK: each user can use their own Tracker without stepping into each other's Tracker"""
        # Arya starts a new skill tracker
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_log')
        input_box.send_keys('Poke the training dummy with needle.')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_text_in_rows_of_table('1. Poke the training dummy with needle.')

        # She notices that her tracker has a unique URL
        arya_tracker_url = self.browser.current_url
        self.assertRegex(arya_tracker_url, '/trackers/.+')

        # Now a new user, Jon Snow, comes to the site
        """Use a new browser session to make sure that no information of Arya's is coming through from cookies etc"""
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Jon visits the home page, there is no sign of Arya's trackers
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('training dummy', page_text)
        self.assertNotIn('cat in the dungeon', page_text)

        # Jon starts a new tracker by entering new log, he is less interesting than Arya
        input_box = self.browser.find_element_by_id('id_new_log')
        input_box.send_keys('Patrol the wall')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_text_in_rows_of_table('1. Patrol the wall')

        # Jon gets his own URL for his tracker
        jon_tracker_url = self.browser.current_url
        self.assertRegex(jon_tracker_url, '/trackers/.+')
        self.assertNotEqual(jon_tracker_url, arya_tracker_url)

        # Again, there's no sign of Arya's logs
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('training dummy', page_text)
        self.assertNotIn('cat in the dungeon', page_text)

        # Satisfied, both of them left.

    def test_layout_and_styling(self):
        """FT-CHECK: layout and styling are generally correct"""
        # Jon Snow goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He noticed the input box is nicely centered
        input_box = self.browser.find_element_by_id('id_new_log')
        # # (x+0.5*w).middlePointInputBox = (1024/2=512).middleScreen +- 10
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # He starts a new Tracker and sees the input box is nicely centered too
        input_box.send_keys('testing layout')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_text_in_rows_of_table('testing layout')
        input_box = self.browser.find_element_by_id('id_new_log')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
