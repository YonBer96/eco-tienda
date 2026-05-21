from django.http import HttpResponse
from django.template.loader import render_to_string


def render_pdf_bytes(template_src, context):
    """Renderiza una plantilla HTML a bytes PDF usando WeasyPrint."""
    try:
        from weasyprint import HTML
    except Exception:
        return None

    html_string = render_to_string(template_src, context)
    return HTML(string=html_string).write_pdf()


def render_pdf(template_src, context, filename="documento.pdf"):
    pdf_file = render_pdf_bytes(template_src, context)
    if pdf_file is None:
        return None

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
