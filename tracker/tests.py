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
        html = response.content.decode('utf8')  # decode raw byte content into utf-8
        # the correct response should be an html page starting with <html>
        self.assertTrue(html.startswith('<html>'))
        # the title of the home page should be Skill Tracker
        self.assertIn('<title>Skill Tracker</title>', html)
        # the response page should end with </html>
        self.assertTrue(html.endswith('</html>'))
