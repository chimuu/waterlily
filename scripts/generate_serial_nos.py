from django.contrib.auth.models import User

from order.models.order import Order


def run_script():
    print("Wait while updating serial nos")
    users = User.objects.all()
    for user in users:
        orders = Order.objects.filter(user=user).order_by('id')
        serial_no = 1
        for order in orders:
            order.serial_no = serial_no
            order.save()
            serial_no += 1