from bapa import models, services

def get_last_payment(user_id):
    """Retrieve latest payment info for user, or return None"""
    latest = models.Payment.latest( user_id=user_id )
    if latest:
        return latest[0]
    return

def record_payment(ipn):
    """
    Handle an instant payment notification from paypal.
    """
    if not services.paypal.verify_ipn(ipn):
        return 'Invalid IPN'

    user = models.User.from_id(ipn['custom'])
    if not user:
        return 'Invalid user'

    # Save all IPNs
    ipn_id = models.Ipn.create(ipn['custom'], ipn)

    if ipn['payment_status'] == 'Completed':
        if ipn['item_name'] == 'Membership Dues':
            models.Payment.create(
                ipn['custom'], # user_id
                ipn['item_name'],
                ipn['payment_gross'],
                ipn['payment_date'],
                ipn_id
            )
        else:
            # todo, Donation, etc.
            pass
