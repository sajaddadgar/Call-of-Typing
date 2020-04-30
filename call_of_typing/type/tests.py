from django.test import TestCase
from .views import register_validation, LCS, is_email_unique


class TypeTest(TestCase):

    def test_register_validation(self):
        first_name = 'Jonathan'
        last_name = 'ive'
        user_name = 'john123'
        pass1 = 'jjj123JJJ'
        pass2 = 'jjj123JJJ'
        email = 'jonathan.ive@outlook.com'
        self.assertEqual(True, register_validation(first_name, last_name, user_name, pass1, pass2, email))

    def test_LCS(self):
        str1 = "qwe"
        str2 = "qrrrwoiu"
        self.assertEqual(2, LCS(str1, str2))

    def test_is_email_unique(self):
        email = 'm.lashkari98@live.com'
        self.assertEqual(True, is_email_unique(email))


