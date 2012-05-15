from django import forms
from models import Book


class BooksImportForm(forms.Form):
    books = forms.CharField(widget=forms.Textarea)

    def parse_input_data_to_title_list(self):
        data_from_form = self.cleaned_data['books']
        normalised_book_titles = []
        for raw_title in data_from_form.split('\n'):
                stripped_title = raw_title.strip()
                if len(stripped_title) > 0:
                    normalised_book_titles.append(stripped_title)
        return normalised_book_titles

class BooksEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title",)
