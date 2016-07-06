import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

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

def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should display on the 
        index page.
        """
        create_question(question_text="Past question.", days = -1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question.>'])

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not display
        on the index page.
        """
        create_question(question_text="Future question.", days = 1)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_past_and_future_questions(self):
        """
        Questions with a pub_date in the past should display on the
        index page. Questions with a pub_date in the future shouldn't
        """
        create_question(question_text="Past question.", days = -1)
        create_question(question_text="Future question.", days = 1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                 response.context['latest_question_list'],
                ['<Question: Past question.>'])

    def test_index_view_with_two_past_questions(self):
        """
        The index view can show multiple questions.
        """
        create_question(question_text="Past question 1.", days = -1)
        create_question(question_text="Past question 2.", days = -2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question 1.>',
                 '<Question: Past question 2.>'])

