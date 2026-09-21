'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple
from decimal import Decimal, InvalidOperation, localcontext

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

MAX_ITEM_AMOUNT = 100000
MAX_QUANTITY = 100
MAX_TOTAL = Decimal('1000000')


def validorder(order: Order):
    # Separate totals avoid losing product costs between a large payment/refund.
    payments = Decimal('0')
    expenses = Decimal('0')
    with localcontext() as context:
        context.prec = 50
        for item in order.items:
            if item.type not in ('payment', 'product'):
                return "Invalid item type: %s" % item.type
            try:
                amount = Decimal(str(item.amount))
            except (InvalidOperation, ValueError):
                return "Invalid item amount"
            if not amount.is_finite() or abs(amount) > Decimal('1e20'):
                return "Invalid item amount"
            if item.type == 'payment':
                payments += amount
            else:
                if (type(item.quantity) is not int or
                        not 0 < item.quantity <= MAX_QUANTITY or
                        not 0 < amount <= MAX_ITEM_AMOUNT):
                    return "Invalid product amount or quantity"
                expenses += amount * item.quantity
            if expenses > MAX_TOTAL:
                return "Total amount payable for an order exceeded"
        if abs(payments) > MAX_TOTAL:
            return "Total amount payable for an order exceeded"
        net = payments - expenses
        if net:
            return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
        return "Order ID: %s - Full payment received!" % order.id
