# pricing_logic.py

from decimal import Decimal, ROUND_DOWN
from .models import Equipment, PriceRuleMin, PriceRuleMax

def calculate_discounted_price(price, product_type, price2=None):
    product_type_instance = Equipment.objects.get(name=product_type)
    price_rules = PriceRuleMin.objects.filter(product_type=product_type_instance)

    for rule in price_rules:
        if rule.price_range_end:
            if rule.price_range_start <= price2 <= rule.price_range_end:
                return rule.apply_discount(price)
        else:
            return rule.apply_discount(price)

    # Default case if no matching rule is found
    return price


def calculate_discounted_price2(price, product_type, price2=None):
    product_type_instance = Equipment.objects.get(name=product_type)
    price_rules = PriceRuleMax.objects.filter(product_type=product_type_instance)

    for rule in price_rules:
        if rule.price_range_end:
            if rule.price_range_start <= price2 <= rule.price_range_end:
                return rule.apply_discount(price)
        else:
            return rule.apply_discount(price)

    # Default case if no matching rule is found
    return price
