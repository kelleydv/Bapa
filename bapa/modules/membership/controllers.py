from bapa import db
from bapa.services import verify_ipn
from bapa.models import User, Profile, Ipn, Payment

from bapa.utils import parse_ratings

import cloudinary
import cloudinary.uploader


def get_user_profile(user_id):
    """Get a user and profile record"""
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    if user:
        setattr(user, 'last_payment', get_last_payment(user_id))
    if profile:
        setattr(profile, 'ratings', parse_ratings(user.ushpa_data))
        if profile.picture:
            cloudinary_id = profile.picture.get('public_id')
            attrs = { #workaround since `class` is a keyword
                'class': 'img-responsive prof',
                'width': 360,
                'crop': 'fill',
            }
            html = cloudinary.CloudinaryImage(cloudinary_id).image(**attrs)
            setattr(profile, 'picture_html', html)
    return user, profile


def update_user_profile(user_id, data):
    """
    Update a users information in both the user and profile tables
    """
    user, profile = get_user_profile(user_id)
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

def upload_profile_picture(user_id, image):
    """Use cloudinary to upload a profile picture"""
    profile = Profile.query.filter_by(user_id=user_id).first()
    profile.picture = cloudinary.uploader.upload(image)
    db.session.add(profile)
    db.session.commit()
    return


def is_member(user_id):
    """
    Determine if someone is a member.
    If they have payed dues in the last year,
    they are a member.
    """
    dues = Payment.query.filter_by(user_id=user_id, item='Membership Dues').order_by(Payment.created_at.desc()).first()
    if dues:
        if not is_too_old(dues.created_at, years=1):
            return True
        return False


def get_last_payment(user_id):
    """Retrieve latest payment info for user, or return None"""
    latest = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).first()
    return latest


def record_payment(ipn):
    """
    Handle an instant payment notification from paypal.
    """
    if not verify_ipn(ipn):
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
