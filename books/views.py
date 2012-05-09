from forms import BooksImportForm
from models import Book

from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import DeleteView

@login_required
def import_books(request):
    if request.method == 'POST':
        form = BooksImportForm(request.POST)
        if form.is_valid():
            rawInputData = form.cleaned_data['books']
            parsedBookList = BooksImportForm.parse_input_data(rawInputData)
            for bookTitle in parsedBookList:
                newBook = Book()
                newBook.title = bookTitle
                newBook.owner = request.user
                newBook.save()
            return HttpResponseRedirect('/books/my') # Redirect after POST
    else:
        form = BooksImportForm() # An unbound form

    return render_to_response('import_books.html', {
        'form': form,
    }, context_instance=RequestContext(request))


class MyBooksListView(ListView):
    context_object_name = 'books'
    template_name = 'books_list.html'

    def get_queryset(self):
        return Book.objects.filter(owner_id=self.request.user.id)

class MyBookDeleteView(DeleteView):
    model = Book
    success_url = '/books/my'

    def get_object(self, queryset=None):
        book = super(MyBookDeleteView, self).get_object()
        if not book.owner == self.request.user:
            raise Http404
        return book
