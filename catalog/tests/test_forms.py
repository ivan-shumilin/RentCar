from django.test import TestCase
from catalog import views

from catalog.models import Cars
from catalog.forms import FindCarsForm
from django.urls import reverse
import datetime
import pdb


class FindCarsFormTest(TestCase):
    fixtures = ['catalog/tests/fixtures/test_bd.json']

    def test_is_valid_custom(self):
        response = self.client.post('/catalog/', data={'date_start': '2022-17-04', 'date_finish': '2022-19-04'})
        self.assertEqual(200, response.status_code)
        # pdb.set_trace()
        # Поиск в html
        # self.assertIn('Извините, пока мы не можем отправить машину в прошлое.', response.content.decode('utf-8'))


