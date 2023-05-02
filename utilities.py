from decimal import Decimal

def decimalize(num):
    if num is None:
        num = 0
    return Decimal(num).quantize(Decimal('0.01'))
