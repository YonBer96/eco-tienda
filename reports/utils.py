from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string


def render_pdf(template_src, context, filename="documento.pdf"):
    try:
        from weasyprint import CSS, HTML
    except Exception:
        return None

    html_string = render_to_string(template_src, context)
    css_path = finders.find("css/reports.css")
    stylesheets = [CSS(filename=css_path)] if css_path else None
    pdf_file = HTML(string=html_string).write_pdf(stylesheets=stylesheets)

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
