from django import forms


class EmailDraftForm(forms.Form):
    to = forms.EmailField(label='Destinatario')
    cc = forms.CharField(label='CC', required=False, help_text='Opcional. Separa varios correos con comas.')
    subject = forms.CharField(label='Asunto', max_length=200)
    body = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'rows': 16}))
