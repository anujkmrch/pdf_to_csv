from django import forms


class DocumentForm(forms.Form):
    title = forms.CharField(label='Query Variable', help_text='Please enter the query variable', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'NPA'}))

    year = forms.CharField(label='Query Year', help_text='Please enter the relevant year.', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '2015'}))

    # for creating file input
    pdf_file = forms.FileField(
        label='Please upload balance sheet', help_text='Only Pdf file allowed!', widget=forms.FileInput(attrs={'accept': 'application/pdf'}))
