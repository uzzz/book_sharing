from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.template.loader import get_template

class ShowDetailView(DetailView):
    template_name = "user_detail.html"
    context_object_name = "user"
    model = User
