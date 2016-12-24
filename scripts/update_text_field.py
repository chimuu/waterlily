from order.models.order import Order


def run_script():
    orders = Order.objects.all()
    for instance in orders:
        instance.save()