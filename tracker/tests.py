from django.test import TestCase  # extends unittest.TestCase
from django.core.urlresolvers import resolve  # for resolving url internally
from django.http import HttpRequest  # for request pages

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
