from django.test import TestCase  # extends unittest.TestCase
from django.core.urlresolvers import resolve  # for resolving url internally
from django.http import HttpRequest  # for request pages

from tracker.views import home_page  # for testing home_page view
# Create your tests here.


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  # found.func is the view function of '/'
        self.assertEqual(found.func, home_page)

    def test_home_page_respond_correct_html(self):
        request = HttpRequest()
        response = home_page(request)  # give home_page a request, return a response
        # the correct response should be an html page starting with <html>
        self.assertTrue(response.content.startswith(b'<html>'))  # response.content is raw bytes, use b'<str>'
        # the title of the home page should be Skill Tracker
        self.assertIn(b'<title>Skill Tracker</title>', response.content)
        # the response page should end with </html>
        self.assertTrue(response.content.endswith(b'</html>'))
