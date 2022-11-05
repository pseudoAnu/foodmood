# my creation
from logging import exception
import profile
from django.http import HttpResponse
from django.shortcuts import render,redirect
from profiles.models import Profile
from posts.models import Post
from posts.models import Like
import pandas as pd
import csv
from autoscraper import AutoScraper
import os
from posts.forms import PostModelForm,CommentModelForm
post_added=False

def index(request):
    return render(request,'index.html')
def feed(request):
    try:
        obj=Profile.objects.get(user=request.user)

        if request.method == 'POST':
        # print(request.POST.get('q'))
            amazon_scraper = AutoScraper()
            amazon_scraper.load('static/amazon1_in.json')
            search = request.POST.get('q')
            amazon_url="https://www.amazon.in/s?k={}".format(search)

            data = amazon_scraper.get_result_similar(amazon_url, group_by_alias=True)
            search_data = tuple(zip(data['Title'],data['ImageUrl'],data['Price']))

            df = pd.DataFrame(columns=['Title','Price','ImageUrl'])
            for i in range(len(search_data)):
                df.loc[len(df)] = [search_data[i][0],search_data[i][-1],search_data[i][-2]]

            df.to_csv("static/searchedData13.csv",index=False)

        csv_fp = open(f'static/searchedData13.csv', 'r')
        reader = csv.DictReader(csv_fp)
        headers = [col for col in reader.fieldnames]
        out = [row for row in reader]

        context={
            'obj':obj,
            'out':out,
            'headers':headers
         }
 
        return render(request,'feed1.html',context)
    except:
        
        csv_fp = open(f'static/searchedData12.csv', 'r')
        reader=csv.DictReader(csv_fp)
        headers = [col for col in reader.fieldnames]
        out = [row for row in reader]

        context={
            'obj':obj,
            'out':out,
            'headers':headers
         }
 
        return render(request,'feed1.html',context)


def myprofile(request):
    global post_added
    obj=Profile.objects.get(user=request.user)   
    qs=Post.objects.all()
    p_form=PostModelForm()
    c_form=CommentModelForm()
    context={
            'obj':obj,
            'qs':qs,
            'p_form':p_form,
            'c_form':c_form,
            'post_added':post_added,
         }
    return render(request,'myprofile.html',context)

def like_unlike_post(request):
    user=request.user
    if request.method=='POST':
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        profile=Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
          post_obj.liked.remove(profile)
        else:
          post_obj.liked.add(profile)
        like,created=Like.objects.get_or_create(user=profile,post_id=post_id)
        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.vlaue='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()
    return redirect('myprofile')

def update_profile(request):
    obj=Profile.objects.get(user=request.user)
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    bio=request.POST.get('bio')
    country=request.POST.get('country')
    if request.method=="POST":
        if len(request.FILES)!=0:
            if len(obj.avatar)>0:
                os.remove(obj.avatar.path)
            obj.avatar=request.FILES['mydp']
        if first_name:
            obj.first_name=first_name
        if last_name:
            obj.last_name=last_name
        if bio:
            obj.bio=bio
        if country:
            obj.country=country
        obj.save()
    return redirect('myprofile')

def new_post(request):
    obj=Profile.objects.get(user=request.user)   
    qs=Post.objects.all()
    #post form,comment  form
    p_form=PostModelForm()
    c_form=CommentModelForm()
    if 'submit_p_form' in request.POST: 
        p_form=PostModelForm(request.POST,request.FILES)
        if p_form.is_valid():
            instance=p_form.save(commit=False)
            instance.author=obj
            instance.save()
            p_form=PostModelForm()
            post_added=True
    #comment form
    if 'submit_c_form' in request.POST:
        c_form=CommentModelForm(request.POST)
        if c_form.is_valid():
            instance=c_form.save(commit=False)
            instance.user=obj
            instance.post=Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form=CommentModelForm()


        
    return redirect('myprofile')
    
       
