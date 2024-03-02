from . import models


def create_order(fio, address, total_price):
    return models.Order.objects.create(
        fio=fio,
        address=address,
        total_price=total_price
    )


def create_order_food(food, order, quantity):
    price = food.price * int(quantity)

    return models.OrderFood(
        food=food,
        order=order,
        quantity=quantity,
        price=price
    )
