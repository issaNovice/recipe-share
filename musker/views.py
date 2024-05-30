from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from .decorators import anonymous_required

def index(request):
	if request.user.is_authenticated:
		return render(request, 'home.html')
	else:
		return render(request, 'index.html')

@login_required(login_url="login")
def home(request):
	if request.user.is_authenticated:
		form = MeepForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				meep = form.save(commit=False)
				meep.user = request.user
				meep.save()
				return redirect('home')
			
		profile = Profile.objects.get(user=request.user)
		meeps = Meep.objects.select_related('user__profile').all().order_by("-created_at")
		return render(request, 'home.html', {"profile": profile, "meeps":meeps, "form":form})
	else:
		meeps = Meep.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"meeps":meeps})

@login_required(login_url="login")
def post_meep(request):
    if request.method == "POST":
        form = MeepForm(request.POST, request.FILES)
        if form.is_valid():
            meep = form.save(commit=False)
            meep.user = request.user
            meep.save()
            return redirect('home')  
        else:
            messages.error(request, "Error posting. Please check your form data.")
    else:
        form = MeepForm()
    return render(request, 'post_meep.html', {'form': form})


@login_required(login_url="login")
def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")

	
		if request.method == "POST":
			current_user_profile = request.user.profile
			action = request.POST['follow']
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			current_user_profile.save()



		return render(request, "profile.html", {"profile":profile, "meeps":meeps})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')		


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})

@login_required(login_url="login")
def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out"))
	return redirect('login')

@anonymous_required(redirect_url='home')
def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})

@login_required(login_url="login")
def liked_posts(request):
    if request.user.is_authenticated:
        liked_meeps = Meep.objects.filter(likes=request.user)
        return render(request, 'liked_posts.html', {'liked_meeps': liked_meeps})
    else:
        messages.error(request, "You must be logged in to view liked posts.")
        return redirect('login')


@login_required(login_url="login")
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')


def meep_like(request, pk):
	if request.user.is_authenticated:
		meep = get_object_or_404(Meep, id=pk)
		if meep.likes.filter(id=request.user.id):
			meep.likes.remove(request.user)
		else:
			meep.likes.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		return redirect('home')


def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        data = {
            'body': meep.body,
            'ingredients': meep.ingredients,
            'procedure': meep.procedure,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Not Exist...'}, status=404)	


@login_required(login_url="login")
def delete_meep(request, pk):
	if request.user.is_authenticated:
		meep = get_object_or_404(Meep, id=pk)
		if request.user.username == meep.user.username:
			meep.delete()
			
			messages.success(request, ("The Recipe Has Been Deleted!"))
			return redirect(request.META.get("HTTP_REFERER"))	
		else:
			messages.success(request, ("You Don't Own That Meep!!"))
			return redirect('home')

	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect(request.META.get("HTTP_REFERER"))



@login_required(login_url="login")
def search(request):
	if request.method == "POST":
		search = request.POST['search']
		searched = Meep.objects.filter(body__contains = search)

		return render(request, 'search.html', {'search':search, 'searched':searched})
	else:
		return render(request, 'search.html', {})