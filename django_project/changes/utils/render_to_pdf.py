import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa


links = lambda uri, rel: \
    os.path.join(
        settings.MEDIA_ROOT,
    uri.replace(settings.MEDIA_URL, '')
    )


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=links)
    # pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result, link_callback=link_callback)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
