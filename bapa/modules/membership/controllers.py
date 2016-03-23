from bapa import db, services
from bapa.models import User, Ipn, Payment

def get_last_payment(user_id):
    """Retrieve latest payment info for user, or return None"""
    latest = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).first()
    return latest

def record_payment(ipn):
    """
    Handle an instant payment notification from paypal.
    """
    if not services.paypal.verify_ipn(ipn):
        return 'Invalid IPN'

    user = User.query.get(ipn['custom'])
    if not user:
        return 'Invalid user'

    # Save all IPNs
    this_ipn = Ipn(ipn['custom'], ipn)
    db.session.add(this_ipn)
    db.session.commit()

    if ipn['payment_status'] == 'Completed':
        if ipn['item_name'] == 'Membership Dues':
            payment = Payment(
                ipn['custom'], # user_id
                ipn['item_name'],
                ipn['payment_gross'],
                ipn['payment_date'],
                this_ipn.id
            )
            db.session.add(payment)
            db.session.commit()
        else:
            # todo, Donation, etc.
            pass
