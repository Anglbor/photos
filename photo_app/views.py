from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout
from django.views import View
from photo_app.models import Photo, Album, Location, Camera, Tag
from django.shortcuts import render, redirect
from .forms import PhotoForm, DisplayForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User


class DisplayView(View):
    def get(self, request):
        photo_list = Photo.objects.filter(sender=request.user.id).order_by('name')
        form =DisplayForm()
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


            # form.save()
            return render(request, "photo_upload.html", {'form': form, 'img_obj': img_obj})
        else:
            form = PhotoForm
        return render(request, "photo_upload.html", {'form': form})







class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

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

#
#
# class Edit_photoView(View):
#     def get(self, request, id):
#         form = EditphotoForm()
#         context = {'form': form}
#         return render(request, "edit_photo.html", context)
#
#     def post(self, request, id):
#         form = EditphotoForm(request.POST)
#         context = {'form': form}
#
#         if form.is_valid():
#             # form.save()
#             # messages.success(request, "Photo changed")
#             return redirect("/photos/")
#
#
#
#
#
#
# class SearchView(View):
#     def get(self, request):
#         form = SearchForm()
#         context = {'form': form}
#
#         return render(request, "search_homework.html", context)
#
#
#     def post(self, request):
#         form = SearchForm(request.POST)
#         # search = request.POST['search']
#         categories=""
#         products =""
#         contex = {
#             "form": form,
#             "products": products,
#             "categories": categories
#         }
#
#         if form.is_valid():  # True/ False
#
#             search_value = form.cleaned_data['search']
#             categories = Category.objects.filter(category_name__icontains=search_value)
#             products = Product.objects.filter(name__icontains=search_value)
#             contex["categories"] = categories
#             contex["products"] = products
#
#
#
#
#
#
#         return render(request, "search_homework.html", contex)
#
