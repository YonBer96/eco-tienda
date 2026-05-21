from django.http import HttpResponse
from django.template.loader import render_to_string


<<<<<<< HEAD
def render_pdf_bytes(template_src, context):
    """Renderiza una plantilla HTML a bytes PDF usando WeasyPrint."""
=======
def render_pdf(template_src, context, filename="documento.pdf"):
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
    try:
        from weasyprint import HTML
    except Exception:
        return None

    html_string = render_to_string(template_src, context)
<<<<<<< HEAD
    return HTML(string=html_string).write_pdf()


def render_pdf(template_src, context, filename="documento.pdf"):
    pdf_file = render_pdf_bytes(template_src, context)
    if pdf_file is None:
        return None

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
=======
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
