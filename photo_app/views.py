import os
from pyexpat.errors import messages

import json

from django.contrib.auth import authenticate, login, logout
from django.views import View
from photo_app.models import Photo, Tag, Display_photos
from django.shortcuts import render, redirect
from .forms import PhotoForm, DisplayForm, SearchForm
from django.contrib import messages


def delete_view(request, id):

    # deleting the photo from database und photos list
    photo = Photo.objects.get(pk=id)
    photo_tags = photo.tag.all()
    if len(photo.photo)>0:
        os.remove(photo.photo.path)
    photo.tag.clear()
    photo.delete()
    messages.success(request, "Photo deleted")


    photo_all = Photo.objects.all()

    for tag in photo_tags:

        # filter search in photo_user by this same tag_name
        tags_in_photos = photo_all.filter(tag__in=tag)

        if tags_in_photos.count() == 0:
            tag.delete()

    return redirect('display')








#shows display photos, which are ordered by id of the user

class DisplayView(View):
    def get(self, request):
        photo_list = Photo.objects.filter(sender=request.user.id).order_by('name')
        form = DisplayForm()
        ctx = {'photo_list': photo_list,
               'form': form}
        # print(photo_list[0].photo.url)

        return render(request, 'display.html', ctx)

    def post(self, request):
        photo_list = Photo.objects.filter(sender=request.user.id).order_by('name')
        form = DisplayForm(request.POST)
        ctx = {'photo_list': photo_list,
               'form': form}
        if form.is_valid():
            return render(request, 'display.html', ctx)


# uploads photos, adding tags to the photos
class Photo_upload_view(View):
    def fx(self, request, form, img_obj=None):
        taglist = []
        js_tags = json.dumps(taglist)
        alltags = [tag.tag_name for tag in Tag.objects.filter(user=request.user.id)]
        js_alltags = json.dumps(alltags)
        ctx = {
            'form': form,
            'img_obj': img_obj,
            'js_tags': js_tags,
            "js_alltags": js_alltags
           }
        return render(request, "photo_upload.html", ctx)

    def get(self, request):

        # Taglist exists due to javascript in template, js expects in a taglist. For uploading a new photo
        # taglist always will be empty (tags do not exist for a new photo yet).
        # taglist = []
        # js_tags = json.dumps(taglist)
        # alltags = [tag.tag_name for tag in Tag.objects.filter(user=request.user.id)]
        # js_alltags = json.dumps(alltags)

        form = DisplayForm()
        return self.fx(request, form)

        # ctx = {
        #     'form': form,
        #     'js_tags': js_tags,
        #     "js_alltags": js_alltags
        # }
        #
        # return render(request, "photo_upload.html", ctx)


    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            img_obj = form.instance
            photo_value = form.cleaned_data['photo']
            name_value = form.cleaned_data['name']
            sender = request.user

            new_photo = Photo.objects.create(name=name_value, photo=photo_value, sender=sender)

            id_value = new_photo.pk

            # Future work should check if the tag fields exists in the request.
            tag_name_list = request.POST['tags'].split(',')

            for tag_name in tag_name_list:
                try:
                    # print(f"attempting to query for tag {tag_name}")
                    tag = Tag.objects.get(user=request.user.id, tag_name=tag_name)
                except Tag.DoesNotExist as e:
                    print(f'tag {tag_name} not found')
                    tag = Tag.objects.create(tag_name=tag_name, user=request.user)
                    print(f'created tag {tag_name}')
                # here 'tag' must exist
                new_photo.tag.add(tag)
            new_photo.save()
            return self.fx(request, form, img_obj)
            # taglist = []
            # js_tags = json.dumps(taglist)
            # alltags = [tag.tag_name for tag in Tag.objects.filter(user=request.user.id)]
            # js_alltags = json.dumps(alltags)
            # ctx = {'form': form,
            #        'img_obj': img_obj,
            #        'js_tags': js_tags,
            #        "js_alltags": js_alltags
            #        }
            # return render(request, "photo_upload.html", ctx)
        else:
            form = PhotoForm
        return self.fx(request, form)
        # taglist = []
        # js_tags = json.dumps(taglist)
        # alltags = [tag.tag_name for tag in Tag.objects.filter(user=request.user.id)]
        # js_alltags = json.dumps(alltags)
        # ctx = {'form': form,
        #        'js_tags': js_tags,
        #        "js_alltags": js_alltags
        #        }
        # return render(request, "photo_upload.html", ctx)






# shows login for user, displays 3 different photos
class LoginView(View):
    def get(self, request):
        image_list = Display_photos.objects.order_by('?')[:3]
        context = {
            "image_list": image_list
        }
        return render(request, "login.html", context)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Log in!")
            return redirect("display")
        else:
            messages.error(request, "Error in password or username")
            return render(request, "login.html")


# logout for the user
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


# displays a single photo
class PhotoView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect("login")

        try:
            photo = Photo.objects.get(pk=id)
        except Photo.DoesNotExist as e:
            return redirect("display")

        if request.user.id != photo.sender.id:
            return redirect("display")
        # print(photo.tag.all())
        # First get a list of all tag names associated with the photo.
        # Remember that photo.tag.all() is a query set, _not_ an actual list. So it
        # needs to be turned into a list using list comprehension.
        taglist = [tag.tag_name for tag in photo.tag.all()]
        # taglist = []
        # for tag in photo.tag.all():
        #     taglist.extend(tag.tag_name)
        # Now turn the tag list into a json object that's readable by javascript.
        js_tags = json.dumps(taglist)
        # Having done this, the text must be marked as safe (even if it's not) so that
        # special characters are not escaped, i.e. {{js_tags|safe}}.
        # Without this, then "door" is given as &quotdoor&quot, which javascript
        # knows nothing about and will error on.

        # Same as above, but show all tags from the currently logged in user.
        alltags = [tag.tag_name for tag in Tag.objects.filter(user=request.user.id)]
        js_alltags = json.dumps(alltags)

        form = DisplayForm()
        ctx = {
            'photo': photo,
            'js_tags': js_tags,
            "js_alltags": js_alltags
        }

        # print(photo_list[0].photo.url)
        return render(request, 'photo.html', ctx)

    def post(self, request, id):
        # Future work should check if the tag fields exists in the request.
        tag_name_list = request.POST['tags'].split(',')

        photo = Photo.objects.get(pk=id)
        photo.tag.clear()

        for tag_name in tag_name_list:
            try:
                # print(f"attempting to query for tag {tag_name}")
                tag = Tag.objects.get(user=request.user.id, tag_name=tag_name)
            except Tag.DoesNotExist as e:
                print(f'tag {tag_name} not found')
                tag = Tag.objects.create(tag_name=tag_name, user=request.user)
                print(f'created tag {tag_name}')
            # here 'tag' must exist
            photo.tag.add(tag)
        photo.save()
        # print(tag_name_list)
        return self.get(request, id)




# searching photos base on tags, and login user

class SearchView(View):
    def get(self, request):
        form = SearchForm()
        alltags = [tag.tag_name for tag in Tag.objects.filter(user=request.user.id)]

        context = {
            'form': form,
            'js_tags': json.dumps([]),
            'js_alltags': json.dumps(alltags)
        }

        return render(request, "search.html", context)

    def post(self, request):
        form = SearchForm(request.POST)
        photos = []
        alltags = [tag.tag_name for tag in Tag.objects.filter(user=request.user.id)]
        ctx = {
            "form": form,
            "photos": photos,
            'js_tags': json.dumps([]),
            'js_alltags': json.dumps(alltags)
        }

        if form.is_valid():  # True/ False
            # list of strings put into the list - splited
            search_tags_list = form.cleaned_data['search'].split(',')
            # search_values = search for search in range(search_value)

            # filted photos by user. Photos being used ony by the user.
            photo_user = Photo.objects.filter(sender=request.user.id)

            # loop of tag_name in the list
            for tag_name in search_tags_list:
                # comepered this some tags from loop and taken from Tag
                tag_in_loop = Tag.objects.filter(tag_name=tag_name)
                # filter search in photo_user by this same tag_name
                photo_user = photo_user.filter(tag__in=tag_in_loop)


            # tags = Tag.objects.filter(tag_name__icontains=search_value)

            # photos = Photo.objects.filter(tag__in=tags).filter(sender=request.user.id).distinct()
            ctx["photos"] = photo_user

        return render(request, "search.html", ctx)
