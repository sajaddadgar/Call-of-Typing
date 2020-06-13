from django.test import TestCase
from .views import register_validation, LCS, is_email_unique, text_in_persian
from .models import OrdinaryText, GroupMembers, GroupAdmin
from django.contrib.auth.models import User, Group


class TypeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='kkkiii',
                                        password='pppiii_987',
                                        first_name='r',
                                        last_name='e',
                                        email='uuuttt@gmail.com')

        self.group = Group.objects.create(name='Gang')
        GroupAdmin.objects.create(group=self.group, admin=self.user)
        GroupMembers.objects.create(group=self.group, user=self.user)

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

    def test_text_rank(self):
        self.assertEqual(1, self.user.profile.get_text_rank())

    def test_song_rank(self):
        self.assertEqual(1, self.user.profile.get_song_rank())

    def test_score_fields(self):
        self.assertEqual(0, self.user.profile.text_score)
        self.assertEqual(0, self.user.profile.song_score)
        self.user.profile.text_score = 20
        self.user.profile.song_score = 30
        self.user.save()
        self.assertEqual(20, self.user.profile.text_score)
        self.assertEqual(30, self.user.profile.song_score)

    def test_group_text_rank(self):
        ga = GroupAdmin.objects.get(group=self.group)
        self.assertEqual(1, ga.get_group_text_rank())

    def test_group_song_rank(self):
        ga = GroupAdmin.objects.get(group=self.group)
        self.assertEqual(1, ga.get_group_song_rank())

    def test_group_member_score_fields(self):
        g_member = GroupMembers.objects.filter(group=self.group, user=self.user)[0]
        self.assertEqual(0, g_member.user_text_score)
        self.assertEqual(0, g_member.user_song_score)

    def test_group_member_text_rank(self):
        g_member = GroupMembers.objects.filter(group=self.group, user=self.user)[0]
        self.assertEqual(1, g_member.get_member_text_rank())

    def test_group_member_song_rank(self):
        g_member = GroupMembers.objects.filter(group=self.group, user=self.user)[0]
        self.assertEqual(1, g_member.get_member_song_rank())

    def test_group_text_score(self):
        ga = GroupAdmin.objects.get(group=self.group)
        self.assertEqual(0, ga.get_group_text_score())
        g_member = GroupMembers.objects.filter(group=self.group, user=self.user)[0]
        g_member.user_text_score = 360
        g_member.save()
        self.assertEqual(360, ga.get_group_text_score())

    def test_group_song_score(self):
        ga = GroupAdmin.objects.get(group=self.group)
        self.assertEqual(0, ga.get_group_song_score())
        g_member = GroupMembers.objects.filter(group=self.group, user=self.user)[0]
        g_member.user_song_score = 18
        g_member.save()
        self.assertEqual(18, ga.get_group_song_score())

    def test_is_admin(self):
        g_member = GroupMembers.objects.filter(group=self.group, user=self.user)[0]
        self.assertEqual(True, g_member.is_admin())



