from django.core.urlresolvers import reverse
from oscar.test import factories

from oscar.test.testcases import WebTestCase
from oscar.core.compat import get_user_model
from oscar.apps.catalogue.models import Product
from oscar.test.factories import (
    CategoryFactory, ProductFactory, ProductClassFactory)

User = get_user_model()


class ProductWebTest(WebTestCase):
    is_staff = True

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@email.com',
                                             password='somefancypassword')
        self.user.is_staff = self.is_staff
        self.user.save()

    def get(self, url, **kwargs):
        kwargs['user'] = self.user
        return self.app.get(url, **kwargs)


class TestGatewayPage(ProductWebTest):
    is_staff = True

    def test_redirects_to_list_page_when_no_query_param(self):
        url = reverse('dashboard:catalogue-product-create')
        response = self.get(url)
        self.assertRedirects(response,
                             reverse('dashboard:catalogue-product-list'))

    def test_redirects_to_list_page_when_invalid_query_param(self):
        url = reverse('dashboard:catalogue-product-create')
        response = self.get(url + '?product_class=bad')
        self.assertRedirects(response,
                             reverse('dashboard:catalogue-product-list'))

    def test_redirects_to_form_page_when_valid_query_param(self):
        pclass = ProductClassFactory(name='Books', slug='books')
        url = reverse('dashboard:catalogue-product-create')
        response = self.get(url + '?product_class=%s' % pclass.pk)
        expected_url = reverse('dashboard:catalogue-product-create',
                               kwargs={'product_class_slug': pclass.slug})
        self.assertRedirects(response, expected_url)


class TestCreateParentProduct(ProductWebTest):
    is_staff = True

    def setUp(self):
        self.pclass = ProductClassFactory(name='Books', slug='books')
        super(TestCreateParentProduct, self).setUp()

    def submit(self, title=None, category=None, upc=None):
        url = reverse('dashboard:catalogue-product-create',
                      kwargs={'product_class_slug': self.pclass.slug})

        product_form = self.get(url).form

        product_form['title'] = title
        product_form['upc'] = upc
        product_form['structure'] = 'parent'

        if category:
            product_form['productcategory_set-0-category'] = category.id

        return product_form.submit()

    def test_title_is_required(self):
        response = self.submit(title='')

        self.assertContains(response, "must have a title")
        self.assertEqual(Product.objects.count(), 0)

    def test_requires_a_category(self):
        response = self.submit(title="Nice T-Shirt")
        self.assertContains(response,
            "must have at least one category")
        self.assertEqual(Product.objects.count(), 0)

    def test_for_smoke(self):
        category = CategoryFactory()
        response = self.submit(title='testing', category=category)
        self.assertIsRedirect(response)
        self.assertEqual(Product.objects.count(), 1)

    def test_doesnt_allow_duplicate_upc(self):
        ProductFactory(parent=None, upc="12345")
        category = CategoryFactory()
        self.assertTrue(Product.objects.get(upc="12345"))

        response = self.submit(title="Nice T-Shirt", category=category,
                               upc="12345")

        self.assertEqual(Product.objects.count(), 1)
        self.assertNotEqual(Product.objects.get(upc='12345').title,
                            'Nice T-Shirt')
        self.assertContains(response,
                            "Product with this UPC already exists.")


class TestCreateChildProduct(ProductWebTest):
    is_staff = True

    def setUp(self):
        self.pclass = ProductClassFactory(name='Books', slug='books')
        self.parent = ProductFactory(structure='parent', stockrecords=[])
        super(TestCreateChildProduct, self).setUp()

    def test_categories_are_not_required(self):
        url = reverse('dashboard:catalogue-product-create-child',
                      kwargs={'parent_pk': self.parent.pk})
        page = self.get(url)

        product_form = page.form
        product_form['title'] = expected_title = 'Nice T-Shirt'
        product_form.submit()

        try:
            product = Product.objects.get(title=expected_title)
        except Product.DoesNotExist:
            self.fail('creating a child product did not work')

        self.assertEqual(product.parent, self.parent)


class TestProductUpdate(ProductWebTest):

    def test_product_update_form(self):
        self.product = factories.ProductFactory()
        url = reverse('dashboard:catalogue-product',
                      kwargs={'pk': self.product.id})

        page = self.get(url)
        product_form = page.form
        product_form['title'] = expected_title = 'Nice T-Shirt'
        page = product_form.submit()

        product = Product.objects.get(id=self.product.id)

        self.assertEqual(page.context['product'], self.product)
        self.assertEqual(product.title, expected_title)
