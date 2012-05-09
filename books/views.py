from django.http import HttpRequest
from forms import BooksImportForm
from django.shortcuts import render_to_response


def import_books(request):
    if request.method == 'POST':
        form = BooksImportForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = BooksImportForm() # An unbound form

    return render_to_response('import_books.html', {
        'form': form,
    })
            