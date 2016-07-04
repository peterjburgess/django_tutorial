import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions
        who have future pub_date
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for question with
        pub_date > 1 day
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for question with
        pub_date < 1 day
        """
        time = timezone.now() - datetime.timedelta(hours=20)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)
