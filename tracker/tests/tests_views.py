"""
The unit tests
    for Skill Tracker
        by Leon (Hao Wu)
"""
from django.test import TestCase  # extends unittest.TestCase
from django.utils.html import escape
from tracker.models import Log, Tracker  # the Log that user inputs to track their skills

# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')  # dj-test.client get page
        # make sure it's using the correct template, only work with response from TestCase.client
        self.assertTemplateUsed(response, 'home.html')


class TrackerViewTest(TestCase):

    def test_uses_tracker_template(self):
        tracker = Tracker.objects.create()
        response = self.client.get(f'/trackers/{tracker.id}/')
        self.assertTemplateUsed(response, 'tracker.html')

    def test_display_only_logs_for_its_tracker(self):
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
        correct_tracker = Tracker.objects.create()
        other_tracker = Tracker.objects.create()
        response = self.client.get(f'/trackers/{correct_tracker.id}/')
        self.assertEqual(response.context['tracker'], correct_tracker)

    def test_can_save_a_POST_log_to_an_existing_tracker(self):
        correct_text = 'A new Log for an existing Tracker'

        # make 2 trackers, compare later
        other_tracker = Tracker.objects.create()
        correct_tracker = Tracker.objects.create()

        # POST a Log to correct Tracker
        self.client.post(
            f'/trackers/{correct_tracker.id}/',
            data={
                'log_text': correct_text
            }
        )

        # a Log created, to the first place, with correct text, to the correct Tracker
        self.assertEqual(Log.objects.count(), 1)
        new_log = Log.objects.first()
        self.assertEqual(new_log.text, correct_text)
        self.assertEqual(new_log.tracker, correct_tracker)

    def test_POST_redirects_to_tracker_view(self):
        correct_text = 'A new Log for an existing Tracker'

        correct_tracker = Tracker.objects.create()
        other_tracker = Tracker.objects.create()

        response = self.client.post(
            f'/trackers/{correct_tracker.id}/',
            data={
                'log_text': correct_text
            }
        )

        expected_url = f'/trackers/{correct_tracker.id}/'
        self.assertRedirects(response, expected_url)

    def test_validation_errors_end_up_on_tracker_page(self):
        tracker = Tracker.objects.create()
        response = self.client.post(
            f'/trackers/{tracker.id}/',
            data={'log_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker.html')
        expected_error = escape("You can't save an empty log.")
        self.assertContains(response, expected_error)

class NewTrackerTest(TestCase):

    def test_can_save_a_POST_request(self):
        # with client, post a new log to db
        self.client.post('/trackers/new', data={
            'log_text': 'A new log item'
        })

        # check if there is 1 log saved in db, and it has the correct text
        self.assertEqual(Log.objects.count(), 1)
        new_log = Log.objects.first()
        self.assertEqual(new_log.text, 'A new log item')

    def test_redirects_after_POST(self):
        # make the POST
        response = self.client.post('/trackers/new', data={
            'log_text': 'A new log item'
        })
        # last inserted Tracker is first
        new_tracker = Tracker.objects.first()
        # check the redirection
        expected_url = f"/trackers/{new_tracker.id}/"
        self.assertRedirects(response, expected_url)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/trackers/new', data={
            'log_text': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = "You can&#39;t save an empty log."
        self.assertContains(response, expected_error)

    def test_invalid_tracker_logs_arent_saved(self):
        self.client.post('/trackers/new', data={
            'log_text': ''
        })
        self.assertEqual(Tracker.objects.count(), 0)
        self.assertEqual(Log.objects.count(), 0)
