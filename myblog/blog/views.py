from django.shortcuts import render
from django.views import generic
from blog.models import Author, Category, Post, Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime
from blog.models import Post

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_posts = Post.objects.all().count()
    num_category = Category.objects.all().count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
        'num_posts': num_posts,
        'num_category': num_category,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class Sort_by_Author(generic.ListView):
    """ Generic class-based view for a list of blogs posted by a particular BlogAuthor."""
    model = Post
    pagnate_by = 5
    template_name = 'blog/posts_by_author.html'

    def get_queryset(self):
        """Return list of Blog objects created by BlogAuthor (author id specified in URL)"""
        id = self.kwargs['pk']
        target_author=get_object_or_404(Author, pk = id)
        return Post.objects.filter(author=target_author)
        
    def get_context_data(self, **kwargs):
        """Add BlogAuthor to context so they can be displayed in the template"""
        # Call the base implementation first to get a context
        context = super(Sort_by_Author, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(Author, pk = self.kwargs['pk'])
        return context

class PostListView(generic.ListView):
    """Generic class-based view for a list of blogs."""
    model = Post
    paginate_by = 5


class PostDetailView(generic.DetailView):
    """ Generic class-based detail view for a post."""
    model = Post

class AuthorDetailView(generic.DetailView):
    """ Generic class-based detail view for a post."""
    model = Author

    
class BloggerListView(generic.ListView):
    """Generic class-based view for a list of bloggers."""
    model = Author
    paginate_by = 5


class CommentCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog comment. Requires login."""
    model = Comment
    fields = ['comment',]

    def get_context_data(self, **kwargs):
        """Add associated blog to form template so can display its title in HTML."""
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """Add author and associated blog to form data before setting it as valid (so it is saved to model)"""
        #Add logged-in user as author of comment
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Post, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """After posting comment return to associated blog."""
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'],})

class PostCreate(CreateView):
    model = Post
    fields = '__all__'
    initial = {'post_date': datetime.today().strftime('%m-%d-%y')}

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'author', 'summary', 'text']

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('posts')