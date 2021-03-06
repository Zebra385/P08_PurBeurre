from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Categories, Products
from .views import SearchProductView


class AccueilPageTestCase(TestCase):
    """
    Test that accueil page returns a 200 if the item exists.
    """
    def test_accueil_page(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)


class CopyrightPageTestCase(TestCase):
    """
    Test that copyright page returns a 200 if the item exists.
    """
    def test_copyright_page(self):
        response = self.client.get(reverse('store:copyright'))
        self.assertEqual(response.status_code, 200)


class SearchProducteTestCase(TestCase):

    def setUp(self):
        """
        We create data in the different tables
        """
        Categories.objects.create(name_category='pate')
        self.category = Categories.objects.get(name_category='pate')
        id_category = int(self.category.id)
        self.name_product = 'Ravioli'
        Products.objects.create(name_product=self.name_product,
                                nutriscore_product="d",
                                categorie_id=id_category)
        Products.objects.create(name_product="Ravioli bio3",
                                nutriscore_product="a",
                                categorie_id=id_category)
        self.product = Products.objects.get(name_product='Ravioli')

    def test_environment_set_in_context(self):
        """
        Test the context data
        """

        request = RequestFactory().get('/', data={'name_product': "Ravioli"})
        view = SearchProductView()
        view.setup(request)
        # we fix the object _list because we do not call
        # SearchProduct as a view
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn('essais', context)
        self.assertIn('name_product', context)

    def test_search_product_page_return_200(self):
        """
        Test that Resultat page returns a 200 if the product exists
        """
        name_product = self.product.name_product
        print('le produit est : ', name_product)
        response = self.client.get(reverse('store:search_product'),
                                   name_product=name_product)
        self.assertEqual(response.status_code, 200)
