from django.test import TestCase

class TestAlwyasFail(TestCase):

    def test_always_fail(self):
        self.assertTrue(False)