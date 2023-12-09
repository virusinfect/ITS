# pricing_logic.py

from decimal import Decimal, ROUND_DOWN
from .models import Equipment, PriceRule
def calculate_discounted_price(price, product_type, price2=None,currency=None):
    product_type_instance = Equipment.objects.get(name=product_type)
    price_rules = PriceRule.objects.filter(product_type=product_type_instance)

    for rule in price_rules:
        if rule.price_range_end:
            if rule.price_range_start <= price2 <= rule.price_range_end:
                return rule.apply_discount(price,currency)
        else:
            return rule.apply_discount(price,currency)

    # Default case if no matching rule is found
    return price


def calculate_discounted_price2(price, product_type, price2=None, currency=None):
    product_type_instance = Equipment.objects.get(name=product_type)
    price_rules = PriceRule.objects.filter(product_type=product_type_instance)

    for rule in price_rules:
        if rule.price_range_end:
            if rule.price_range_start <= price2 <= rule.price_range_end:
                return rule.apply_discount2(price,currency)
        elif rule.price_range_end is None:
            return rule.apply_discount2(price,currency)

    # Default case if no matching rule is found
    return price
