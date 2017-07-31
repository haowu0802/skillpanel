"""
The unit tests
    for Skill Tracker
        by Leon (Hao Wu)
"""
from django.test import TestCase  # extends unittest.TestCase
from django.core.urlresolvers import resolve  # for resolving url internally
from django.http import HttpRequest  # for request pages

from tracker.models import Log  # the Log that user inputs to track their skills

from tracker.views import home_page  # for testing home_page view
# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')  # dj-test.client get page
        # make sure it's using the correct template, only work with response from TestCase.client
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        """check: POST data is saved as orm"""
        self.client.post('/', data={
            'log_text': 'A new log item'
        })  # use client to post to / with a new log data, and get response

        self.assertEqual(Log.objects.count(), 1)  # check if there is 1 log saved in db
        new_log = Log.objects.first()
        self.assertEqual(new_log.text, 'A new log item')  # correct text?

    def test_redirects_after_POST(self):
        """, and redirect(302) to / after save"""
        response = self.client.post('/', data={
            'log_text': 'A new log item'
        })
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertEqual(response['location'], '/')  # to /

    def test_only_saves_log_when_necessary(self):
        """check: no log is saved when home page is visited"""
        self.client.get('/')
        self.assertEqual(Log.objects.count(), 0)

    def test_display_all_log_items(self):
        Log.objects.create(text='log1')  # setup 2 logs
        Log.objects.create(text='log2')

        response = self.client.get('/')  # exercise the page

        self.assertIn('log1', response.content.decode())  # assert the results
        self.assertIn('log2', response.content.decode())


class LogModelTest(TestCase):

    def test_saving_and_retrieving_logs(self):
        # create and save 1st log
        first_log = Log()
        first_log.text = 'The first (ever) log item'
        first_log.save()
        # create and save 2nd log
        second_log = Log()
        second_log.text = 'Log the second'
        second_log.save()
        # get all 2 logs and see if we have 2
        saved_logs = Log.objects.all()
        self.assertEqual(saved_logs.count(), 2)
        # specifically check each log
        first_saved_log = saved_logs[0]
        second_saved_log = saved_logs[1]
        # to see if they have the correct content
        self.assertEqual(first_saved_log.text, 'The first (ever) log item')
        self.assertEqual(second_saved_log.text, 'Log the second')
