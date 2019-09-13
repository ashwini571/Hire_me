from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import PostForm, ImagePostForm
from .models import ImagePost, Post
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.utils.timezone import now


def error404(request):
    return render(request, 'error404.html', context={"title": "NOT Found"})


def image_view(request, identifier):
    try:
        img = get_object_or_404(ImagePost, slug=identifier)
        return render(request, 'view_image.html', context={'title': 'Image Post', 'image_post': img})
    except:
        return redirect('feed:404')


def blog_view(request, identifier):
    try:
        post = get_object_or_404(Post, slug=identifier)
        permission = True if post.author == request.user else False
        return render(request, 'view_post.html', {'title': "{}'s Blog".format(request.user.first_name), 'post': post,
                                                  'permission': permission})
    except:
        return redirect('feed:404')


@login_required(login_url='login/')
def create_post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        author = request.user
        created_on = now()
        slug = "{}-blog-{}".format(author.username, slugify(str(created_on)))
        post = Post.objects.create(title=title, content=content, image=image, author=author,
                                   created_on=created_on, updated_on=created_on, slug=slug)
        post.save()
        return redirect(post.get_absolute_url())
    else:
        form = PostForm()
        return render(request, 'new_post.html', context={'title': 'Add Post', 'form': form})


@login_required(login_url='login/')
def create_image_post_view(request):
    if request.method == 'POST':
        image = request.FILES['image']
        content = request.POST.get('caption')
        posted_by = request.user
        created_on = now()
        slug = "{}-image-{}".format(request.user.username,
                                    slugify(str(created_on)))
        img = ImagePost.objects.create(image=image, posted_by=posted_by, slug=slug,
                                       caption=content, created_on=created_on)
        img.save()
        return redirect(img.get_absolute_url())
    else:
        form = ImagePostForm()
        return render(request, 'new_image.html', context={'title': "Add Image", 'form': form})
