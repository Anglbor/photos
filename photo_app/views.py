from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout
from django.views import View
from photo_app.models import Photo, Tag, Display_photos
from django.shortcuts import render, redirect
from .forms import PhotoForm, DisplayForm, SearchForm
from django.contrib import messages


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
        form =DisplayForm(request.POST)
        ctx = {'photo_list': photo_list,
               'form': form}
        if form.is_valid():
            return render(request, 'display.html', ctx)

class Photo_upload_view(View):
    def get(self, request):
        form = PhotoForm()
        return render(request, "photo_upload.html", {'form': form})

    def post(self, request):

        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            context = {'form': form}

            img_obj = form.instance

            photo_value = form.cleaned_data['photo']
            name_value = form.cleaned_data['name']
            tag_set = form.cleaned_data['tags']
            sender = request.user

            new_photo = Photo.objects.create(name=name_value, photo=photo_value, sender=sender)

            id_value = new_photo.pk

            # tag_query_set = Tag.objects.filter(tag_name=tag_name)
            for tag in tag_set:
                new_photo.tag.add(tag)
            new_photo.tag.save()


            # form.save()
            return render(request, "photo_upload.html", {'form': form, 'img_obj': img_obj})
        else:
            form = PhotoForm
        return render(request, "photo_upload.html", {'form': form})







class LoginView(View):
    def get(self, request):
        image_list =Display_photos.objects.order_by('?')[:3]
        context = {
            "image_list" : image_list
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



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")



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
        form = DisplayForm()
        ctx = {
            'photo': photo
        }

        # print(photo_list[0].photo.url)

        return render(request, 'photo.html', ctx)









class SearchView(View):
    def get(self, request):
        form = SearchForm()
        context = {'form': form}

        return render(request, "search.html", context)

    def post(self, request):
        form = SearchForm(request.POST)
        photos =""
        contex = {
            "form": form,
            "photos": photos
        }

        if form.is_valid():  # True/ False

            search_value = form.cleaned_data['search']
            tags = Tag.objects.filter(tag_name__icontains=search_value)
            photos = Photo.objects.filter(tag__in=tags).filter(sender=request.user.id).distinct()
            # contex["tags"] = tags
            contex["photos"] = photos

        return render(request, "search.html", contex)

