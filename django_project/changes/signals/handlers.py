from django.utils.translation import ugettext_noop as _
from django.conf import settings
from changes import (
    NOTICE_SUSTAINING_MEMBER_CREATED,
    NOTICE_SUSTAINING_MEMBER_APPROVED,
    NOTICE_SUSTAINING_MEMBER_REJECTED,
    NOTICE_SUSTAINING_MEMBER_UPDATED,
    NOTICE_SUBSCRIPTION_CREATED,
    NOTICE_SUBSCRIPTION_UPDATED,
    NOTICE_TOP_UP_SUCCESS
)


def create_notice_types(sender, **kwargs):
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print("Creating notices for changes")
        NoticeType.create(NOTICE_SUSTAINING_MEMBER_CREATED,
                          _("Sustaining Member Created"),
                          _("A sustaining member has been created"))
        NoticeType.create(NOTICE_SUSTAINING_MEMBER_UPDATED,
                          _("Sustaining Member Updated"),
                          _("A sustaining member has been updated"))
        NoticeType.create(NOTICE_SUSTAINING_MEMBER_REJECTED,
                          _("Sustaining Member Rejected"),
                          _("A sustaining member has been rejected"))
        NoticeType.create(NOTICE_SUSTAINING_MEMBER_APPROVED,
                          _("Sustaining Member Approved"),
                          _("A sustaining member has been approved"))
        NoticeType.create(NOTICE_SUBSCRIPTION_CREATED,
                          _("Subscription Created"),
                          _("A subscription has been created"))
        NoticeType.create(NOTICE_SUBSCRIPTION_UPDATED,
                          _("Subscription Updated"),
                          _("A subscription has been updated"))
        NoticeType.create(NOTICE_TOP_UP_SUCCESS,
                          _("Top Up Successful"),
                          _("Top Up Successful"))
    else:
        print("Skipping creation of NoticeTypes as notification app not found")
