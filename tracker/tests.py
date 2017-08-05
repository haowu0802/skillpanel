"""
The unit tests
    for Skill Tracker
        by Leon (Hao Wu)
"""
from django.test import TestCase  # extends unittest.TestCase
from django.core.urlresolvers import resolve  # for resolving url internally
from django.http import HttpRequest  # for request pages

from tracker.models import Log, Tracker  # the Log that user inputs to track their skills

from tracker.views import home_page  # for testing home_page view
# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')  # dj-test.client get page
        # make sure it's using the correct template, only work with response from TestCase.client
        self.assertTemplateUsed(response, 'home.html')


class LogAndTrackerModelTest(TestCase):
    """test functions of Log and Tracker models"""
    def test_saving_and_retrieving_logs(self):
        """check save and read functions"""
        # create and save associated tracker
        tracker = Tracker()
        tracker.save()

        # create and save 2 logs
        first_log = Log()
        first_log.text = 'The first (ever) log item'
        first_log.tracker = tracker
        first_log.save()
        second_log = Log()
        second_log.text = 'Log the second'
        second_log.tracker = tracker
        second_log.save()

        # check if saved logs and tracker are correct
        saved_tracker = Tracker.objects.first()
        self.assertEqual(saved_tracker, tracker)
        saved_logs = Log.objects.all()
        self.assertEqual(saved_logs.count(), 2)

        # check each log and see if they have the correct properties
        first_saved_log = saved_logs[0]
        second_saved_log = saved_logs[1]
        self.assertEqual(first_saved_log.text, 'The first (ever) log item')
        self.assertEqual(first_saved_log.tracker, tracker)
        self.assertEqual(second_saved_log.text, 'Log the second')
        self.assertEqual(second_saved_log.tracker, tracker)


class TrackerViewTest(TestCase):

    def test_uses_tracker_template(self):
        """CHECK: tracker view use tracker tpl"""
        response = self.client.get('/trackers/the-only-tracker/')
        self.assertTemplateUsed(response, 'tracker.html')

    def test_display_all_logs(self):
        """CHECK: logs created will show in tracker view"""
        # create 2 Logs and their Tracker
        tracker = Tracker.objects.create()
        Log.objects.create(text='log1', tracker=tracker)
        Log.objects.create(text='log2', tracker=tracker)

        response = self.client.get('/trackers/the-only-tracker/')  # exercise the page

        self.assertContains(response, 'log1')  # assertContains deals with content decoding, http code, etc.
        self.assertContains(response, 'log2')


class NewTrackerTest(TestCase):
    """tests for creating new tracker"""
    def test_can_save_a_POST_request(self):
        """CHECK: POST data is saved as orm"""
        # with client, post a new log to db
        self.client.post('/trackers/new', data={
            'log_text': 'A new log item'
        })

        # check if there is 1 log saved in db, and it has the correct text
        self.assertEqual(Log.objects.count(), 1)
        new_log = Log.objects.first()
        self.assertEqual(new_log.text, 'A new log item')

    def test_redirects_after_POST(self):
        """CHECK: redirect works after POST"""
        # make the POST
        response = self.client.post('/trackers/new', data={
            'log_text': 'A new log item'
        })
        # check the redirection
        expected_url = "/trackers/the-only-tracker/"
        assert isinstance(response, object)
        self.assertRedirects(response, expected_url)
