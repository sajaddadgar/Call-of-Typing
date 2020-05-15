from django.test import TestCase
from .views import register_validation, LCS, is_email_unique, text_in_persian
from .models import OrdinaryText

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

    def test_text_in_persian(self):
        my_text_1 = "Hello  *** Hi"
        my_text_2 = "سلام من اینجا هستم"
        self.assertEqual(False, text_in_persian(my_text_1))
        self.assertEqual(True, text_in_persian(my_text_2))

    def test_ord_text_content_field(self):
        new_text = "Hello I am here"
        text_obj = OrdinaryText.objects.create(content=new_text)
        self.assertEqual(text_obj.content, new_text)
