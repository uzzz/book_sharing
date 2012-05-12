from django import forms
from models import Book


class BooksImportForm(forms.Form):
    books = forms.CharField(widget=forms.Textarea)

    @staticmethod
    def parse_input_data(DataFromForm):
        rawBookTitles = DataFromForm.split('\n',1)
        normalisedBookTitles = []
        for rawTitle in rawBookTitles:
            strippedTitle = rawTitle.strip()
            normalisedBookTitles.append(strippedTitle)

        return normalisedBookTitles

class BooksEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title",)