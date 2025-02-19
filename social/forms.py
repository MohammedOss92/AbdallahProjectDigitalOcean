from django import forms
from .models import *

class Post2Form(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':'Say Something...'
        })
    )
    #add
    image = forms.ImageField(required = False)
    class Meta:
        model = Post
        #fields = ['body']
        fields = ['body','image']
 
#multi img        
class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
            })
    )

    class Meta:
        model = Post
        fields = ['body']
        


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))
        
    #add image
    image = forms.ImageField(required=False)  # ????? ??? ??????

    class Meta:
        model = Comment
        fields = ['comment','image']
        
class CommentRepForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))
        
    #image = forms.ImageField(required=False)

    class Meta:
        model = Comment
        fields = ['comment']
        





class ThreadForm(forms.Form):
    username = forms.CharField(label='',max_length=100)
    
    
class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']





class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))
            
            



class ExploreForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder':'Explore tags'
        })
    )
    
    

class Co2mmentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))
        
    # ??? ??????
    image = forms.ImageField(required=False)

    class Meta:
        model = Comment
        fields = ['comment', 'image']

    def __init__(self, *args, **kwargs):
        parent = kwargs.get('parent', None)  # ???? ??? ???? parent ??? ???? ??????
        super(CommentForm, self).__init__(*args, **kwargs)
        
        # ??? ??? ??????? ?? ?? (?? ????? ??? parent)? ???? ?????? ??? ??????
        if parent:
            self.fields['image'].widget = forms.HiddenInput()  # ????? ?????
            self.fields['image'].required = False  # ?????? ?? ?? ????? ??? ???????


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)  # ????? ??? username
    email = forms.EmailField(required=True)  # ????? ??? email

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'bio', 'birth_date', 'location', 'picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email 

    def clean_username(self):
        # ?????? ?? ?? `username` ??? ????
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username
    def clean_email(self):
        # ?????? ?? ?? `email` ??? ????
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise ValidationError("This email is already in use. Please choose another one.")
        return email


        