# from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.shortcuts import redirect, render
# from django.contrib.auth import authenticate, login, logout
# from .forms import  EditProfileForm
# from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
# from .forms import *
# from .models import *
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt,csrf_protect
# from django.core import serializers
#
# # Create your views here.
#
# def getUser(id):
#     return SheltuzUser.objects.filter(id=id).first()
#
# def index(request):
#     advert = advert = AD.objects.all().order_by('-created_at')
#     location = Location.objects.all()
#     categories = Category.objects.all()
#
#
#     context = {
#         'locations':location,
#         'adverts':advert,
#         'categories':categories,
#         'top_categories':categories.filter(is_top_category=True).exclude(image__isnull=True)[:4],
#         'chosen_categories': categories[:1]
#     }
#     return render(request,"index.html", context)
#
#
# def register(request):
#     if request.method == "POST":
#         form = SheltuzUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             SheltuzUser.objects.create(
#                 user=User.objects.filter(email=form.cleaned_data.get('email')).first(),
#                 phone_number=form.cleaned_data.get('phone_number')
#             )
#
#             return redirect("signin")
#     else:
#         form = SheltuzUserForm()
#     return render(request,"accounts/register.html", {"form":form})
#
#
#
# def register_ajax(request):
#     success=False
#     message=""
#
#     if request.method == 'POST':
#         form = SheltuzUserForm(request.POST)
#         print("FORM_DETAILS: ", request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password1')
#
#                 user = authenticate(username=username, password=password)
#
#                 SheltuzUser.objects.create(
#                     user=user,
#                     phone_number=form.cleaned_data.get('phone_number')
#                 )
#
#                 login(request, user)
#
#                 # print("SHELTUZ_USER", user.id, SheltuzUser.objects.filter(id=request.user.id))
#
#                 success=True
#                 message=f"Registration was successful, welcome {request.POST['username']}"
#
#
#             except Exception as e:
#                 print(e)
#                 message="Something went wrong, please try again"
#
#             data = {
#                 "success": success,
#                 "message": message
#             }
#
#             return JsonResponse(data, status=200)
#
#
# @login_required
# def profile(request):
#         if request.method == "POST":
#             user = SheltuzUser.objects.filter(id=user.id).first()
#             form = EditProfileForm(request.POST, instance=request.user)
#             if form.is_valid():
#                 user.email = form.cleaned_data.get('email')
#                 user.phone_number = form.cleaned_data.get('phone_number')
#                 user.save()
#                 form.save()
#                 messages.success(request, 'Your profile is updated successfully')
#                 return redirect("account")
#         else:
#             form = EditProfileForm(instance=request.user)
#         return render(request, "accounts/editprofile.html", {"editform":form})
#
# def profile(request):
#         if request.method == "POST":
#             form = PasswordChangeForm(request.POST, instance=request.user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Your profile is updated successfully')
#                 return redirect("account")
#         else:
#             form = PasswordChangeForm(instance=request.user)
#         return render(request, "accounts/change-password.html", {"changepassword":form})
#
# def signin(request):
#     if request.method == "POST":
#         form_data=request.POST
#         username = form_data['username']
#         password = form_data['password']
#         form = AuthenticationForm(data = request.POST)
#         if form.is_valid():
#                 user = authenticate(username=username, password=password)
#                 login(request, user)
#                 print("DATA USERNAME={} PASSWORD={}".format(username, password))
#
#                 return redirect('index')
#
#     else:
#         form = AuthenticationForm()
#     return render(request,"accounts/signin.html", {"form":form})
#
# def signin_ajax(request):
#     success = False
#     message = ""
#     if request.method == "POST":
#         first_name = request.POST['first_name']
#         password = request.POST['password']
#
#         form = AuthenticationForm(data=request.POST)
#
#         if form.is_valid():
#             try:
#                 user = authenticate(username=username, password=password)
#                 login(request, user)
#                 success=True
#                 message='Login was successful'
#
#                 print("USER_ID: ", user.id)
#                 s_user = SheltuzUser.objects.filter(id=user.id).first()
#                 print("SHELTUZ_USER: ", s_user)
#
#             except Exception as e:
#                 print(str(e))
#                 message = 'Login failed, please try again'
#
#         data = {
#             "success": success,
#             "message": message
#         }
#
#         return JsonResponse(data, status=200)
#
#
# def account(request):
#     category = Category.objects.all()
#     form = EditProfileForm(instance=request.user)
#     passwordform = PasswordChangeForm(user=request.user)
#
#     context = {
#         "changepassword":passwordform,
#         'categories': category,
#         'editform':form
#     }
#
#     return render(request,"accounts/account.html" , context)
#
# def signout(request):
#     logout(request)
#     return redirect('index')
#
#
# # ADS
# def ad_details(request, slug):
#     category = Category.objects.all()
#     q = AD.objects.filter(slug__iexact=slug)
#     if q.exists():
#        q = q.first()
#     else:
#        return HttpResponse('<h1>AD Not Found</h1>')
#     related_ads=AD.objects.filter(category=q.category).exclude(slug=slug)[:8]
#     context = {
#                 'related':related_ads,
#                 'categories': category,
#                 "ad": q,
#                 }
#     return render(request, "adverts/ad_details.html", context)
#
# @login_required
# def my_ads(request):
#
#     sheltuz_user = SheltuzUser.objects.filter(user=request.user).first()
#     ads = AD.objects.filter(author=sheltuz_user)
#     context = {
#         "my_ads": ads,
#     }
#
#     return render(request, "adverts/my_ads.html", context)
#
#
# @csrf_exempt
# def create_ad(request):
#     form = ADsForm()
#     print("Invoked")
#     if request.method == "POST":
#         if request.POST['csrfmiddlewaretoken']:
#             form = ADsForm(request.POST, request.FILES)
#             author = SheltuzUser.objects.filter(user=request.user).first()
#
#             if form.is_valid:
#                 title = request.POST.get("title")
#                 description = request.POST.get("description")
#                 image = request.FILES['image']
#                 gallery_image_1 = request.FILES['gallery_image_1']
#                 gallery_image_2 = request.FILES['gallery_image_2']
#                 gallery_image_3 = request.FILES['gallery_image_3']
#                 price = request.POST.get('price')
#                 category = request.POST.get('category')
#                 has_warranty = request.POST.get('has_warranty')
#                 condition = request.POST.get('condition')
#                 location = request.POST.get('location')
#                 further_location = request.POST.get('further_location')
#
#                 print(location, category)
#
#
#
#                 ad = AD()
#                 ad.title = title
#                 ad.description = description
#                 ad.image = image
#                 ad.gallery_image_1=gallery_image_1
#                 ad.gallery_image_2=gallery_image_2
#                 ad.gallery_image_3=gallery_image_3
#                 ad.price = price
#                 ad.category = Category.objects.filter(id=category).first() or None
#                 ad.has_warranty = True if has_warranty == "on" else False
#                 ad.condition = condition
#                 ad.location = Location.objects.filter(id=location).first()
#                 ad.further_location = further_location
#                 ad.author = author
#
#                 ad.save()
#                 # form.save(commit=False)
#                 # form.author = author
#                 # form.save()
#
#
#                 return redirect('my_ads')
#
#     context = {
#         "form":form,
#         "login_form": AuthenticationForm(),
#         "register_form": SheltuzUserForm()
#     }
#
#     return render(request, "adverts/create_update_ad.html", context)
#
# @login_required
# def update_ad(request, id):
#     ad = AD.objects.filter(id=id).first()
#     user = getUser(request.user.id)
#
#     if user is not ad.author:
#         return redirect('my_ads')
#
#
#     form = ADsForm(instance=ad)
#
#     if request.method == "POST":
#         form = ADsForm(request.POST, instance=ad)
#
#         if form.is_valid:
#             form.save()
#             return redirect('update_ad')
#
#     context = {
#         "form":form
#     }
#
#     return render(request, "adverts/create_update_ad.html", context)
