from django import forms
from .models import Schedule, Sportsman


class InviteSportsmenForm(forms.ModelForm):
    sportsmen = forms.ModelMultipleChoiceField(
        queryset=Sportsman.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите спортсменов'
    )

    
    class Meta:
        model = Schedule
        fields = ['training_type', 'start_time', 'finish_time', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'finish_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-control'
