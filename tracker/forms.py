from django import forms
from tracker.models import Log

EMPTY_LOG_ERROR = "You can't save an empty log."


class LogForm(forms.models.ModelForm):

    class Meta:
        model = Log
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': 'Enter a log.',
                    'class': 'form-control input-lg',
                }
            )
        }
        error_messages = {
            'text': {'required': EMPTY_LOG_ERROR}
        }

