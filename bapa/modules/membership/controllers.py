from bapa import db, services
from bapa.models import User, Profile, Ipn, Payment

def get_user_profile(user_id):
    """Get a profile record"""
    return Profile.query.filter_by(user_id=user_id).first()

def update_user_profile(user_id, data):
    """
    Update a users information in both the user and profile tables
    """
    user = User.query.get(user_id)
    profile = get_user_profile(user_id)
    if not profile:
        profile = Profile(user_id)

    for field in data:
        #TODO: Validate
        if hasattr(profile, field):
            setattr(profile, field, data[field])
        elif hasattr(user, field):
            setattr(user, field, data[field])
        else:
            raise Exception('fuk dat: ' + field)

    db.session.add(user)
    db.session.add(profile)
    db.session.commit()



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
                datetime.strptime(ipn['payment_date'],'%H:%M:%S %b %d, %Y %Z'),
                this_ipn.id
            )
            db.session.add(payment)
            db.session.commit()
        else:
            # todo, Donation, etc.
            pass
