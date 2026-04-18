from django import forms
from .models import ImageTranscription

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageTranscription
        fields = ['image', 'custom_prompt']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
            'custom_prompt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: Enter specific instructions (e.g., "Format as a CSV", "Extract only names", "Convert to JSON")',
                'help_text': 'Enter any specific instructions for processing the transcribed text'
            })
        }

class TextFormatForm(forms.Form):
    CAPITALIZE_CHOICES = [
        ('all', 'ALL CAPS'),
        ('title', 'Title Case'),
        ('sentence', 'Sentence case'),
    ]
    
    capitalization = forms.ChoiceField(
        choices=CAPITALIZE_CHOICES,
        initial='all',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

class CustomPromptForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your custom question or instruction...\nExamples:\n- "Extract only the names"\n- "Format as a numbered list"\n- "Translate to Spanish"\n- "Summarize in 50 words"'
        }),
        label='Custom Instruction/Question',
        help_text='Ask anything about the transcribed text or how you want it formatted'
    )
