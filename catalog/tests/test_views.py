from django.test import TestCase


from catalog.models import Cars
from django.urls import reverse

class CarsListViewTest(TestCase):

    @classmethod
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalog/cars/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('cars'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('cars'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'catalog/cars_list.html')
