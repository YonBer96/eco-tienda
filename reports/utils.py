from django.http import HttpResponse
from django.template.loader import render_to_string


def render_pdf(template_src, context, filename="documento.pdf"):
    try:
        from weasyprint import HTML
    except Exception:
        return None

    html_string = render_to_string(template_src, context)
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response