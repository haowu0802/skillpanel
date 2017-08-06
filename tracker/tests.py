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
        """CHECK: home page uses correct tpl"""
        response = self.client.get('/')  # dj-test.client get page
        # make sure it's using the correct template, only work with response from TestCase.client
        self.assertTemplateUsed(response, 'home.html')


class LogAndTrackerModelTest(TestCase):
    def test_saving_and_retrieving_logs(self):
        """CHECK: can save and read functions"""
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
        """CHECK: Tracker view uses Tracker tpl"""
        tracker = Tracker.objects.create()
        response = self.client.get(f'/trackers/{tracker.id}/')
        self.assertTemplateUsed(response, 'tracker.html')

    def test_display_only_logs_for_its_tracker(self):
        """CHECK: only display Logs for its own Tracker"""
        # create 2 Logs in the correct Tracker
        correct_tracker = Tracker.objects.create()
        Log.objects.create(text='log1 correct', tracker=correct_tracker)
        Log.objects.create(text='log2 correct', tracker=correct_tracker)
        # create 2 Logs in other Tracker
        other_tracker = Tracker.objects.create()
        Log.objects.create(text='log1 other', tracker=other_tracker)
        Log.objects.create(text='log2 other', tracker=other_tracker)

        response = self.client.get(f'/trackers/{correct_tracker.id}/')

        # assertContains deals with content decoding, http code, etc.
        self.assertContains(response, 'log1 correct')
        self.assertContains(response, 'log2 correct')
        self.assertNotContains(response, 'log1 other')
        self.assertNotContains(response, 'log2 other')

    def test_passes_correct_tracker_to_tpl(self):
        """CHECK: the correct Tracker is passed to tpl"""
        correct_tracker = Tracker.objects.create()
        other_tracker = Tracker.objects.create()
        response = self.client.get(f'/trackers/{correct_tracker.id}/')
        self.assertEqual(response.context['tracker'], correct_tracker)


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
        # last inserted Tracker is first
        new_tracker = Tracker.objects.first()
        # check the redirection
        expected_url = f"/trackers/{new_tracker.id}/"
        self.assertRedirects(response, expected_url)


class NewLogTest(TestCase):
    def test_can_save_a_POST_log_to_an_existing_tracker(self):
        """CHECK: POST a Log to an existing Tracker and save"""
        correct_text = 'A new Log for an existing Tracker'
        # make 2 trackers, compare later
        other_tracker = Tracker.objects.create()
        correct_tracker = Tracker.objects.create()

        # POST a Log to correct Tracker
        self.client.post(
            f'/trackers/{correct_tracker.id}/add_log',
            data={
                'log_text': correct_text
            }
        )

        # a Log created, to the first place, with correct text, to the correct Tracker
        self.assertEqual(Log.objects.count(), 1)
        new_log = Log.objects.first()
        self.assertEqual(new_log.text, correct_text)
        self.assertEqual(new_log.tracker, correct_tracker)

    def test_redirects_to_tracker_view(self):
        """CHECK: redirect to Tracker view after POST"""
        correct_text = 'A new Log for an existing Tracker'

        correct_tracker = Tracker.objects.create()
        other_tracker = Tracker.objects.create()

        response = self.client.post(
            f'/trackers/{correct_tracker.id}/add_log',
            data={
                'log_text': correct_text
            }
        )

        expected_url = f'/trackers/{correct_tracker.id}/'
        self.assertRedirects(response, expected_url)
