from django import forms
from .models import Chat


class ChatModelForm(forms.ModelForm):
    """
    This class takes a base class ModelForm that
    lets it create a Form class based on a Django model.
    """

    class Meta:
        model = Chat
        fields = [
            "message",
        ]