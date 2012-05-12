from forms import BooksImportForm, BooksEditForm
from models import Book
from core.mixins import LoginRequiredMixin

from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectMixin

@login_required
def import_books(request):
    if request.method == 'POST':
        form = BooksImportForm(request.POST)
        if form.is_valid():
            rawInputData = form.cleaned_data['books']
            parsedBookList = BooksImportForm.parse_input_data(rawInputData)
            for bookTitle in parsedBookList:
                newBook = Book(title = bookTitle, owner = request.user)
                newBook.save()
            return HttpResponseRedirect('/books/my') # Redirect after POST
    else:
        form = BooksImportForm() # An unbound form

    return render_to_response('import_books.html', {
        'form': form,
    }, context_instance=RequestContext(request))

class AllBooksListView(ListView):
    context_object_name = 'books'
    template_name = 'all_books_list.html'

    def get_queryset(self):
        return Book.objects.all()

class MyBookMixin(LoginRequiredMixin, SingleObjectMixin):

    def dispatch(self, *args, **kwargs):
        return super(MyBookMixin, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        book = super(MyBookMixin, self).get_object()
        if not book.owner == self.request.user:
            raise Http404
        return book

class MyBooksListView(LoginRequiredMixin, ListView):
    context_object_name = 'books'
    template_name = 'my_books_list.html'

    def get_queryset(self):
        return Book.objects.filter(owner_id=self.request.user.id)

class MyBookUpdateView(UpdateView, MyBookMixin):
    model = Book
    template_name = "book_form.html"
    success_url = '/books/my/'
    form_class = BooksEditForm

class MyBookDeleteView(DeleteView, MyBookMixin):
    model = Book
    success_url = '/books/my/'
