from django.test import TestCase  # extends unittest.TestCase
from django.core.urlresolvers import resolve  # for resolving url internally

from tracker.views import home_page  # for testing home_page view
# Create your tests here.


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  # found.func is the view function of '/'
        self.assertEqual(found.func, home_page)
