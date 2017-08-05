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


class TrackerViewTest(TestCase):

    def test_uses_tracker_template(self):
        """if tracker view use tracker tpl"""
        response = self.client.get('/trackers/the-only-tracker/')
        self.assertTemplateUsed(response, 'tracker.html')

    def test_display_all_logs(self):
        """if logs created will show in tracker view"""
        Log.objects.create(text='log1')  # setup 2 logs
        Log.objects.create(text='log2')

        response = self.client.get('/trackers/the-only-tracker/')  # exercise the page

        self.assertContains(response, 'log1')  # assertContains deals with content decoding, http code, etc.
        self.assertContains(response, 'log2')


class NewTrackerTest(TestCase):
    """tests for creating new tracker"""
    def test_can_save_a_POST_request(self):
        """check: POST data is saved as orm"""
        # with client, post a new log to db
        self.client.post('/trackers/new', data={
            'log_text': 'A new log item'
        })

        # check if there is 1 log saved in db, and it has the correct text
        self.assertEqual(Log.objects.count(), 1)
        new_log = Log.objects.first()
        self.assertEqual(new_log.text, 'A new log item')

    def test_redirects_after_POST(self):
        """check redirect works after POST"""
        # make the POST
        response = self.client.post('/trackers/new', data={
            'log_text': 'A new log item'
        })
        # check the redirection
        expected_url = "/trackers/the-only-tracker/"
        assert isinstance(response, object)
        self.assertRedirects(response, expected_url)
