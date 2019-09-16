from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import PostForm, ImagePostForm
from .models import ImagePost, Post, Comment
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from .utils import create_action


def error404(request):
    return render(request, 'error404.html', context={"title": "NOT Found"})


def image_view(request, identifier):
    try:
        img = get_object_or_404(ImagePost, slug=identifier)
        comments = img.comments.all().order_by('created')
        return render(request, 'view_image.html', context={'title': 'Image Post', 'image_post': img,
                                                           'comments': comments})
    except Exception as e:
        print(e)
        return redirect('feed:404')


def blog_view(request, identifier):
    try:
        post = get_object_or_404(Post, slug=identifier)
        permission = True if post.author == request.user else False
        comments = post.comments.all()
        return render(request, 'view_post.html', {'title': "{}'s Blog".format(post.author.first_name), 'post': post,
                                                  'permission': permission, 'comments': comments})
    except Exception as e:
        print(e)
        return redirect('feed:404')


@login_required(login_url='login/')
def photo_ko_like_karo(request, identifier):
    if request.method == 'POST':

        image_obj = ImagePost.objects.get(slug=identifier)
        if request.POST.get('action') == 'like':
            image_obj.likes.add(request.user)
            image_obj.save()
            create_action(request.user, "liked a image", image_obj)
            return redirect(image_obj.get_absolute_url())
        else:
            image_obj.likes.remove(request.user)
            image_obj.save()
            return redirect(image_obj.get_absolute_url())
    else:
        return redirect('feed:404')


@login_required(login_url='login/')
def blog_ko_like_karo(request, identifier):
    if request.method == 'POST':

        obj = Post.objects.get(slug=identifier)
        if request.POST.get('action') == 'like':
            obj.likes.add(request.user)
            obj.save()
            create_action(request.user, "liked a blog post", obj)
            return redirect(obj.get_absolute_url())
        else:
            obj.likes.remove(request.user)
            obj.save()
            return redirect(obj.get_absolute_url())
    else:
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
        create_action(request.user, "added a new post", post)
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
        create_action(request.user, "added an image", img)
        return redirect(img.get_absolute_url())
    else:
        form = ImagePostForm()
        return render(request, 'new_image.html', context={'title': "Add Image", 'form': form})


@login_required(login_url='login/')
@require_POST
def create_comments_view(request):
    slug = request.POST.get('slug')
    ctype = request.POST.get('comment_type')
    comment = request.POST.get('comments')
    if ctype == 'blog':
        blog_post = Post.objects.get(slug=slug)
        comment_instance = Comment.objects.create(user=request.user, body=comment, content_object=blog_post)
        comment_instance.save()
        create_action(request.user, "commented on {} {}'s blog".format(blog_post.author.first_name,
                                                                       blog_post.author.last_name), blog_post)
        return redirect(blog_post.get_absolute_url())
    else:
        image_post = ImagePost.objects.get(slug=slug)
        comment_instance = Comment.objects.create(user=request.user, body=comment, content_object=image_post)
        comment_instance.save()
        create_action(request.user, "commented on {} {}'s image".format(image_post.posted_by.first_name,
                                                                        image_post.posted_by.last_name), image_post)
        return redirect(image_post.get_absolute_url())
