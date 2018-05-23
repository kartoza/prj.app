"""Model admin class definitions.

Note these admin models inherit reversion (which provides history for a model).

..note:: if you add reversion.VersionAdmin to a model be sure to do
    ``./manage.py createinitialrevisions``.

.. see also:: https://github.com/etianen/django-reversion/wiki#getting
    -started-with-django-reversion

"""

from django.contrib import admin
from stripe_payment.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    """Admin for the payment model."""
    list_display = (
        'id', 'model_url', 'model_name',
        'payment_id', 'description', 'amount', 'currency')
    list_filter = ('model_name', 'time_transaction')
    search_fields = ('model_name', 'description',)
    ordering = ('-time_transaction',)

    def model_url(self, obj):
        return '<a href="/site-admin/%s/%s/%s/">%s</a>' % (
            obj.model_app_label.lower(),
            obj.model_name.lower(),
            obj.model_id,
            obj.model_id
        )

    model_url.allow_tags = True
    model_url.short_description = 'Model url'


admin.site.register(Payment, PaymentAdmin)
