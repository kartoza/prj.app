from djstripe import webhooks


# Occurs whenever a card or source will expire at the end of the month.
@webhooks.handler('customer.source.expiring')
def subscription_expiring(event, **kwargs):
    print('We should probably notify the user at this point')


# Occurs whenever a customer's subscription ends.
@webhooks.handler('customer.subscription.deleted')
def subscription_deleted(event, **kwargs):
    print('Triggered webhook ' + event.type)


# Occurs whenever a subscription changes
# (e.g., switching from one plan to another, or
# changing the status from trial to active).
@webhooks.handler('customer.subscription.updated')
def subscription_updated(event, **kwargs):
    from django.contrib.auth.models import User
    user = User.objects.get(id=event.customer.subscriber_id)

    print('Triggered webhook {event} for user {user}'.format(
        event=event.type,
        user=user.username
    ))


# Occurs whenever a customer is signed up for a new plan.
@webhooks.handler('customer.subscription.created')
def subscription_created(event, **kwargs):
    print('Subscription created')
