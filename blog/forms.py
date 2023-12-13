from django import forms
from .models import Comment,Category
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset = Comment.objects.all())
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
        )
        self.fields['parent'].label =''
        self.fields['parent'].required = False
    class Meta:
        model = Comment
        fields = ( 'content', 'parent','rate', 'post')
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '2', 'placeholder':'Enter your comment...'})
        }

    def save(self, *args, **kwarsgs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwarsgs)
    
    