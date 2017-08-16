"""
The unit tests
    for Skill Tracker
        by Leon (Hao Wu)
"""
from django.test import TestCase  # extends unittest.TestCase
from django.core.exceptions import ValidationError
from tracker.models import Log, Tracker  # the Log that user inputs to track their skills

# Create your tests here.


class LogAndTrackerModelTest(TestCase):
    def test_saving_and_retrieving_logs(self):
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

    def test_cannot_save_empty_log_items(self):
        tracker = Tracker.objects.create()
        log = Log(tracker=tracker, text='')
        with self.assertRaises(ValidationError):
            log.save()
            log.full_clean()

    def test_get_absolute_url(self):
        tracker = Tracker.objects.create()
        self.assertEqual(tracker.get_absolute_url(), '/trackers/%d/' % (tracker.id,))
