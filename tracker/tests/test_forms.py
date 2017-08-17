from django.test import TestCase
from tracker.forms import LogForm, EMPTY_LOG_ERROR


class LogFormTest(TestCase):

    def test_form_renders_log_text_input(self):
        form = LogForm()
        self.fail(form.as_p())

    def test_form_input_has_placeholder_and_css_classes(self):
        form = LogForm()
        self.assertIn('placeholder="Enter a log."', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_log(self):
        form = LogForm(data={
            'text': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LOG_ERROR])

