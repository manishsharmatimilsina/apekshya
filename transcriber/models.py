from django.db import models
from django.utils import timezone

class ImageTranscription(models.Model):
    image = models.ImageField(upload_to='transcriptions/', null=True, blank=True)
    original_text = models.TextField(null=True, blank=True)
    formatted_text = models.TextField(null=True, blank=True)
    capitalized_text = models.TextField(null=True, blank=True)
    custom_prompt = models.TextField(null=True, blank=True, help_text="Custom instructions for processing the text")
    custom_response = models.TextField(null=True, blank=True, help_text="Response to custom prompt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Image Transcription'
        verbose_name_plural = 'Image Transcriptions'

    def __str__(self):
        return f"Transcription {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class TranscriptionImage(models.Model):
    transcription = models.ForeignKey(ImageTranscription, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='transcriptions/')
    page_number = models.PositiveIntegerField(default=1)
    individual_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['page_number']
        verbose_name = 'Transcription Image'
        verbose_name_plural = 'Transcription Images'

    def __str__(self):
        return f"Image {self.page_number} of Transcription {self.transcription.id}"
