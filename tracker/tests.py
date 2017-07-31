"""
The unit tests
    for Skill Tracker
        by Leon (Hao Wu)
"""
from django.test import TestCase  # extends unittest.TestCase
from django.core.urlresolvers import resolve  # for resolving url internally
from django.http import HttpRequest  # for request pages

from tracker.models import Log

from tracker.views import home_page  # for testing home_page view
# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')  # dj-test.client get page
        # make sure it's using the correct template, only work with response from TestCase.client
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        # use client to post to / with a new log data, and get response
        response = self.client.post('/', data={
            'log_text': 'A new log item'
        })
        # check to see if the new log item is in the response
        self.assertIn('A new log item', response.content.decode())
        # check again if using the right tpl
        self.assertTemplateUsed(response, 'home.html')


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
