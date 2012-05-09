from forms import BooksImportForm

from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Book


@login_required
def import_books(request):
    if request.method == 'POST':
        form = BooksImportForm(request.POST)
        if form.is_valid():
            newBook = Book()
            newBook.title = form.books
            newBook.owner = reques.user
            newBook.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = BooksImportForm() # An unbound form

    return render_to_response('import_books.html', {
        'form': form,
    }, context_instance=RequestContext(request))
