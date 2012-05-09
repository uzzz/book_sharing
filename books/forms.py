from django import forms

class BooksImportForm(forms.Form):
    books = forms.CharField(widget=forms.Textarea)