from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput, label="Title", min_length=1)
    content = forms.CharField(widget=forms.Textarea, label="Content", min_length=1)

    def clean(self):
        super(newEntry, self).clean()

        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')

        if len(title) < 1:
            self._errors['title'] = self.error_class([
                'Title cannot be empty.'])
        if len(content) < 1:
            self._errors['title'] = self.error_class([
                'Content cannot be empty.'])
            
        return self.cleaned_data
    
class EditEntryForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.old_content = kwargs.pop('old_content')
        super(editEntry, self).__init__(*args,**kwargs)
        self.fields['content'].initial = self.old_content

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': '20', 'cols': '50'}), label="Content", min_length=1)

    def clean(self):
        super(editEntry, self).clean()

        content = self.cleaned_data.get('content')

        if len(content) < 1:
            self._errors['content'] = self.error_class([
                'Content cannot be empty.'])
        
        return self.cleaned_data
