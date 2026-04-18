from django.contrib import admin
from .models import ImageTranscription


@admin.register(ImageTranscription)
class ImageTranscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'is_processed', 'status_badge')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('original_text', 'formatted_text', 'custom_prompt')
    readonly_fields = ('created_at', 'updated_at', 'original_text', 'formatted_text', 'capitalized_text', 'custom_response')
    fieldsets = (
        ('Image', {
            'fields': ('image',)
        }),
        ('Transcription Results', {
            'fields': ('original_text', 'formatted_text', 'capitalized_text')
        }),
        ('Custom Processing', {
            'fields': ('custom_prompt', 'custom_response'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_processed', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        if obj.is_processed and obj.original_text:
            return '✓ Completed'
        elif obj.error_message:
            return '✗ Error'
        else:
            return '⏳ Processing'
    status_badge.short_description = 'Status'
