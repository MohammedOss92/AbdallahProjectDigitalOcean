from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse

#https://chatgpt.com/c/6727bffc-3928-8010-bdb5-eaf84d4eaeb9

class P1ostListView(LoginRequiredMixin, View):
    #def get(self, request, *args, **kwargs):
  #  posts = Post.objects.all().order_by('-created_on')
 #   form = PostForm()

#    context = {
#        'post_list': posts,
#        'form': form,
#    }
#    return render(request, 'social/post_list.html', context)

    
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm()
        share_form =ShareForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        #posts = Post.objects.all().order_by('-created_on')
        #add
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        #form = PostForm(request.POST)
        #add
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)
        
        
        
class PostListView(LoginRequiredMixin, View):

    #def get(self, request, *args, **kwargs):
  #  posts = Post.objects.all().order_by('-created_on')
 #   form = PostForm()

#    context = {
#        'post_list': posts,
#        'form': form,
#    }
#    return render(request, 'social/post_list.html', context)
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        )
        form = PostForm()
        share_form = ShareForm()

        context = {
            'post_list': posts,
            'shareform': share_form,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        )
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        share_form = ShareForm()

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'post_list': posts,
            'shareform': share_form,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)


class PostDetailView2(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        
        #add
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        #add
        notification = Notification.objects.create(notification_type=2,from_user=request.user,to_user=post.author,post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        #form = CommentForm(request.POST)
        #add image
        form = CommentForm(request.POST, request.FILES) 

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            
            new_comment.create_tags()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)
        
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST, request.FILES)  # إضافة request.FILES

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()

            # عرض رسالة نجاح
            #messages.success(request, "تم إضافة التعليق بنجاح.")
        else:
            # عرض رسالة خطأ مع تفاصيل الأخطاء
            #messages.error(request, "حدث خطأ أثناء إضافة التعليق.")
            for error in form.errors.values():
                messages.error(request, error)
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

        
        

class CommentReplyView(LoginRequiredMixin,View):
    def post(self,request,post_pk,pk,*args,**kwargs):
        post =Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentRepForm(request.POST)
        #add image
        #form = CommentForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post 
            new_comment.parent = parent_comment
            new_comment.save()
            
            # فحص قيمة الحقل image للتأكد من أنه تم رفع الصورة
            print("Comment Image:", new_comment.image)  # تحقق من قيمة الحقل image
            if new_comment.image:
                print("Image URL:", new_comment.image.url)  # طباعة رابط الصورة

            
            
        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)
        
        return redirect('post-detail',pk=post_pk)
    



class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class ProfileView2(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        followers = profile.followers.all()
        following_count = UserProfile.objects.filter(followers=profile.user).count()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'following_count': following_count,
            'is_following': is_following,
        }

        return render(request, 'social/profile.html', context)
        
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        # استخدام get_object_or_404 للحصول على الكائن
        profile = get_object_or_404(UserProfile, pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        followers = profile.followers.all()
        following_count = UserProfile.objects.filter(followers=profile.user).count()

        # التحقق مما إذا كان المستخدم يتابع الملف الشخصي
        is_following = request.user in followers

        number_of_followers = followers.count()

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'following_count': following_count,
            'is_following': is_following,
        }

        return render(request, 'social/profile.html', context)

class ProfileEditView2(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
        
        
        


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'social/profile_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user  # تمرير المستخدم الحالي إلى النموذج
        return kwargs

    def form_valid(self, form):
        user = form.instance.user
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user



    def form_invalid(self, form):
        print(form.errors)  # طباعة الأخطاء للتحقق
        return super().form_invalid(form)



    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})



    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


    
def check_availability(request):
    field_type = request.GET.get('field_type', None)
    value = request.GET.get('value', None)

    if field_type == 'username':
        is_available = not User.objects.filter(username=value).exists()
    elif field_type == 'email':
        is_available = not User.objects.filter(email=value).exists()
    else:
        is_available = False

    return JsonResponse({'is_available': is_available})




class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        
        #add
        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            #add
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)
            #add
            notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=post.author, post=post)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            #add
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)
            #add
            notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=comment.author, comment=comment)


        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        
        

class SharedPostView(View):
    def post(self, request,pk, *args, **kwargs):
        original_post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST)
        
        if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get('body'),
                body = original_post.body,
                author = original_post.author,
                created_on = original_post.created_on,
                shared_user = request.user,
                shared_on = timezone.now(),
                
            ) 
            
            new_post.save()
            
            for img in original_post.image.all():
                new_post.image.add(img)
            new_post.save()
        return redirect('post-list')
            


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query) | Q(user__email__icontains=query)
        )

        context = {
            'profile_list': profile_list,
        }

        return render(request, 'social/search.html', context)

class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'social/followers_list.html', context)
        
        
class FollowingListView(View):
    def get(self, request, pk):
        # استرجاع ملف التعريف الخاص بالمستخدم الحالي
        profile = get_object_or_404(UserProfile, pk=pk)
        
        # استرجاع قائمة الأشخاص الذين يتابعهم المستخدم
        following_list = UserProfile.objects.filter(followers=profile.user)
        
        # إعداد السياق لإرساله إلى القالب
        context = {
            'profile': profile,
            'following_list': following_list,
        }
        
        return render(request, 'social/following_list.html', context)
        
        


class PostNotification(View):
    def get(self,request,notification_pk,post_pk,*args,**kwargs):
        notification = Notification.objects.get(pk = notification_pk)
        post = Post.objects.get(pk=post_pk)
        
        notification.user_has_seen =True
        notification.save()
        
        return redirect('post-detail',pk=post_pk)
        
        
        
class FollowNotification(View):
    def get(self,request,notification_pk,profile_pk,*args,**kwargs):
        notification = Notification.objects.get(pk = notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)
        
        notification.user_has_seen =True
        notification.save()
        
        return redirect('profile',pk=profile_pk)
        
        
class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)
        
        
        
        
        
class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')        
        
        
        
        
class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'social/inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'social/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username')
            return redirect('create-thread')
                
        
        
class ThreadView(View):
    def get(self,request,pk,*args,**kwargs):
        form = MessageForm()
        thread =ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        
        context = {
            'thread':thread,
            'form':form,
            'message_list':message_list
        }
        
        return render(request,'social/thread.html',context)        
        
        
        
        
        
        
class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        ##add image form
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()
         #comm img    
        #message = MessageModel(
        #    thread=thread,
        #    sender_user=request.user,
        #    receiver_user=receiver,
        #    body=request.POST.get('message')
        #)

        #message.save()
        
        notification = Notification.objects.create(
            notification_type=4,
            from_user= request.user,
            to_user = receiver,
            thread = thread
        )
        return redirect('thread', pk=pk)        
        
        
        
        
        



class Explore(View):
    def get(self, request, *args, **kwargs):
        explore_form = ExploreForm()
        query = self.request.GET.get('query', '').strip()  # إزالة المسافات الزائدة

        if query:  # إذا كان هناك استعلام
            tag = Tag.objects.filter(name__icontains=query).first()
            if tag:
                posts = Post.objects.filter(tags__in=[tag])
            else:
                posts = Post.objects.all()  # في حال لم يتم العثور على وسم مطابق
        else:
            posts = Post.objects.all()  # إذا لم يكن هناك استعلام، عرض كل المنشورات

        context = {
            'tag': tag if query else None,  # تعيين الوسم فقط إذا كان هناك استعلام
            'posts': posts,
            'explore_form': explore_form,
            'no_results': not posts.exists() and not query,  # إذا لم تكن هناك نتائج
        }

        return render(request, 'social/explore.html', context)

    def post(self, request, *args, **kwargs):
        explore_form = ExploreForm(request.POST)
        if explore_form.is_valid():
            query = explore_form.cleaned_data['query'].strip()  # إزالة المسافات الزائدة
            if query:
                tag = Tag.objects.filter(name__icontains=query).first()
                if tag:
                    posts = Post.objects.filter(tags__in=[tag])

                    if not posts.exists():
                        messages.error(request, 'No posts found for this tag.')
                        return redirect('explore')  # إعادة التوجيه إلى صفحة البحث
                else:
                    messages.error(request, 'Tag not found.')
                    return redirect('explore')  # إعادة التوجيه إلى صفحة البحث
                
                # إعادة التوجيه مع الاستعلام في URL
                return redirect(f'/social/explore?query={query}')
            else:
                messages.error(request, 'Invalid search query.')
                return redirect('explore')
        
        # إذا كانت البيانات المدخلة في النموذج غير صالحة
        messages.error(request, 'Invalid search query.')
        return redirect('explore')






