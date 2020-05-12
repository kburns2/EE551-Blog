from django.db import models
from datetime import date
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User #Blog author or commenter


# Create your models here.

class Author(models.Model):
    '''Model representing the Blogs Author'''
    name = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=500, help_text="Enter your bio about you")

    class Meta:
        ordering = ['name', 'bio']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('posts-by-author', args=[str(self.id)])

    def get_nonabsolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name.username


class Category(models.Model):
    '''Model representing the type of Blog Post'''
    name = models.CharField(max_length=100, help_text='Enter a category (e.g. Travel, Personal, Cooking)')
    def __str__(self):
        '''String represnting the Model object'''
        return self.name

class Post(models.Model):
    '''Model representing the Blog Post'''
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=100, help_text='Enter a brief description of the blog')
    text = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateField(default=date.today)
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    category = models.ManyToManyField(Category, help_text='Select a Category for this blog')
    
    class Meta:
        ordering = ['-post_date'] #newest to oldest
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('post-detail', args=[str(self.id)])



class Comment(models.Model):
    '''Model representing the Blogs Comments'''
    comment = models.TextField(max_length = 100, help_text="Enter a comment about the blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["post_date"]
    
    def __str__(self):
        """String for representing the Model object."""
        len_title=75
        if len(self.comment)>len_title:
            titlestring=self.comment[:len_title] + '...'
        else:
            titlestring=self.comment
        return titlestring
