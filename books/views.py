from forms import BooksImportForm, BooksEditForm
from models import Book
from core.mixins import LoginRequiredMixin

from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectMixin

@login_required
def import_books(request):
    if request.method == 'POST':
        form = BooksImportForm(request.POST)
        if form.is_valid():
            for book_title in form.parse_input_data_to_title_list():
                new_book = Book(title = book_title, owner = request.user)
                new_book.save()
            return HttpResponseRedirect('/books/my') # Redirect after POST
    else:
        form = BooksImportForm() # An unbound form

    return render_to_response('import_books.html', {
        'form': form,
    }, context_instance=RequestContext(request))

class AllBooksListView(ListView):
    context_object_name = 'books'
    template_name = 'all_books_list.html'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AllBooksListView, self).get_context_data(**kwargs)
        books = [
            {
                'book': book,
                'requestable': book.is_available_for_request(self.request.user)
            } for book in self.get_queryset()
            ]
        context[self.context_object_name] = books

        return context

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

class BookRequestView(View, SingleObjectMixin, LoginRequiredMixin):
    model = Book
    success_url = '/books/all/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.request(request.user)

        return HttpResponseRedirect(self.success_url)
