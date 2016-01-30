from decimal import Decimal as D
import json
import requests

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from oscar.core import prices
from oscar.apps.shipping.abstract_models import AbstractWeightBased
from apps.rajaongkir_cities.models import RajaongkirCity


class Base(object):
    """
    Shipping method interface class

    This is the superclass to the classes in methods.py, and a de-facto
    superclass to the classes in models.py. This allows using all
    shipping methods interchangeably (aka polymorphism).

    The interface is all properties.
    """

    #: Used to store this method in the session.  Each shipping method should
    #  have a unique code.
    code = '__default__'

    #: The name of the shipping method, shown to the customer during checkout
    name = 'Default shipping'

    #: A more detailed description of the shipping method shown to the customer
    #  during checkout.  Can contain HTML.
    description = ''

    #: Whether the charge includes a discount
    is_discounted = False

    def calculate(self, basket):
        """
        Return the shipping charge for the given basket
        """
        raise NotImplemented()

    def discount(self, basket):
        """
        Return the discount on the standard shipping charge
        """
        return D('0.00')


class Free(Base):
    """
    This shipping method specifies that shipping is free.
    """
    code = 'free-shipping'
    name = _('Free shipping')

    def calculate(self, basket):
        # If the charge is free then tax must be free (musn't it?) and so we
        # immediately set the tax to zero
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('0.00'), tax=D('0.00'))


class NoShippingRequired(Free):
    """
    This is a special shipping method that indicates that no shipping is
    actually required (eg for digital goods).
    """
    code = 'no-shipping-required'
    name = _('No shipping required')


class FixedPrice(Base):
    """
    This shipping method indicates that shipping costs a fixed price and
    requires no special calculation.
    """
    code = 'fixed-price-shipping'
    name = _('Fixed price shipping')

    # Charges can be either declared by subclassing and overriding the
    # class attributes or by passing them to the constructor
    charge_excl_tax = None
    charge_incl_tax = None

    def __init__(self, charge_excl_tax=None, charge_incl_tax=None):
        if charge_excl_tax is not None:
            self.charge_excl_tax = charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = charge_incl_tax

    def calculate(self, basket):
        return prices.Price(
            currency=basket.currency,
            excl_tax=self.charge_excl_tax,
            incl_tax=self.charge_incl_tax)


class OfferDiscount(Base):
    """
    Wrapper class that applies a discount to an existing shipping
    method's charges.
    """
    is_discounted = True

    def __init__(self, method, offer):
        self.method = method
        self.offer = offer

    # Forwarded properties

    @property
    def code(self):
        return self.method.code

    @property
    def name(self):
        return self.method.name

    @property
    def discount_name(self):
        return self.offer.name

    @property
    def description(self):
        return self.method.description

    def calculate_excl_discount(self, basket):
        return self.method.calculate(basket)


class TaxExclusiveOfferDiscount(OfferDiscount):
    """
    Wrapper class which extends OfferDiscount to be exclusive of tax.
    """

    def calculate(self, basket):
        base_charge = self.method.calculate(basket)
        discount = self.offer.shipping_discount(base_charge.excl_tax)
        excl_tax = base_charge.excl_tax - discount
        return prices.Price(
            currency=base_charge.currency,
            excl_tax=excl_tax)

    def discount(self, basket):
        base_charge = self.method.calculate(basket)
        return self.offer.shipping_discount(base_charge.excl_tax)


class TaxInclusiveOfferDiscount(OfferDiscount):
    """
    Wrapper class which extends OfferDiscount to be inclusive of tax.
    """

    def calculate(self, basket):
        base_charge = self.method.calculate(basket)
        discount = self.offer.shipping_discount(base_charge.incl_tax)
        incl_tax = base_charge.incl_tax - discount
        excl_tax = self.calculate_excl_tax(base_charge, incl_tax)
        return prices.Price(
            currency=base_charge.currency,
            excl_tax=excl_tax, incl_tax=incl_tax)

    def calculate_excl_tax(self, base_charge, incl_tax):
        """
        Return the charge excluding tax (but including discount).
        """
        if incl_tax == D('0.00'):
            return D('0.00')
        # We assume we can linearly scale down the excl tax price before
        # discount.
        excl_tax = base_charge.excl_tax * (
            incl_tax / base_charge.incl_tax)
        return excl_tax.quantize(D('0.01'))

    def discount(self, basket):
        base_charge = self.method.calculate(basket)
        return self.offer.shipping_discount(base_charge.incl_tax)


class JNEReguler(AbstractWeightBased):
    def __init__(self, basket, shipping_addr):
        self.shipping_addr = shipping_addr
        self.basket = basket

    code = 'JNE reguler'
    name = 'JNE reguler'

    def get_cost(self, origin_id, destination_name, weight):
        destination = RajaongkirCity.objects.get(city_name=destination_name)
        destination = destination.city_id
        payload = {'origin': origin_id, 'destination': destination, 'weight': weight, 'courier': 'jne'}

        headers = {
            'key': settings.RAJAONGKIR_KEY,
            'content-type': "application/x-www-form-urlencoded"
        }

        r = requests.post('http://api.rajaongkir.com/starter/cost', data=payload, headers=headers)
        parsed = json.loads(r.text)
        for shipping_type in parsed['rajaongkir']['results'][0]['costs']:
            if shipping_type['service'] == 'REG':
                return shipping_type['cost'][0]['value']

    def calculate(self, basket):
        # Note, when weighing the basket, we don't check whether the item
        # requires shipping or not.  It is assumed that if something has a
        # weight, then it requires shipping.
        weight = 0
        for line in basket.lines.all():
            weight += line.product.weight * line.quantity
        print weight
        cost = self.get_cost(settings.SHIPPING_ORIGIN, self.shipping_addr.city, weight)

        return prices.Price(
            currency=basket.currency,
            excl_tax=D(cost), incl_tax=D(cost))