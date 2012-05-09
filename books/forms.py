from django import forms

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
