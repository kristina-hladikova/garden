from typing import Optional

from zahradka_app.models import UserMembership, Membership


def get_user_membership(user) -> Optional[Membership]:
    user_membership_qs = UserMembership.objects.filter(user=user)
    if user_membership_qs.exists():
        return user_membership_qs.first().membership

    return None