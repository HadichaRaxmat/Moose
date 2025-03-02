from django.contrib.sites import requests
from django.shortcuts import render, redirect
from .models import Post, Contact, Comment
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

BOT_TOKEN = '7049827349:AAEGygN8m8c0wyMm8NjBHw5uSA2OSNtMGCg'
CHAT_ID = '7072790607'


def home_view(request):
    posts = Post.objects.filter(is_published=True).order_by('-view_count')[:2]
    d = {
        'posts': posts,
        'comments': Comment.objects.all(),
        'home': 'active'
    }
    return render(request, 'index.html', context=d)


def blog_view(request):
    data = request.GET
    cat = data.get('cat', None)
    page = data.get('page', 1)
    if cat:
        posts = Post.objects.filter(is_published=True, category_id=cat)
        d = {
            'posts': posts,
            'blog': 'active',
        }
        return render(request, 'blog.html', context=d)

    posts = Post.objects.filter(is_published=True)
    page_obj = Paginator(posts, 3)

    d = {
        'blog': 'active',
        'posts': page_obj.get_page(page)
    }
    return render(request, 'blog.html', context=d)


def about_view(request):
    return render(request, 'about.html', context={'about': 'active'})


def contact_view(request):
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(full_name=data['name'], email=data['email'],
                                     subject=data['subject'], message=data['message'])
        obj.save()
        text = f"""
        project: MOOSE \nid: {obj.id} \nname: {obj.full_name} \nemail: {obj.email} \nsubject: {obj.subject} 
        \nmessage: {obj.message} \ntimestamp: {obj.created_at}
        """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        response = requests.get(url)
        print(response)
        return redirect('/contact')
    return render(request, 'contact.html', context={'contact': 'active'})


def blog_detail_view(request, id):
    if request.method == 'POST':
        data = request.POST
        comment = Comment.objects.create(post_id=id, name=data['name'], email=data['email'], message=data['message'])
        comment.save()
        return redirect(f'/blog/{id}/')
    post = Post.objects.get(id=id)
    post.view_count += 1
    post.save(update_fields=['view_count'])
    comments = Comment.objects.filter(post_id=id, is_published=True)
    return render(request, 'blog-single.html', {'post': post, 'comments': comments, 'blog': 'active'})


@receiver(post_save, sender=Comment)
def update_post_comments_count(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = Comment.objects.filter(post=post).count()
    post.save(update_fields=['comments_count'])
