from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
import json

from .models import ImageTranscription
from .forms import ImageUploadForm, TextFormatForm, CustomPromptForm
from .services import TranscriptionService


def index(request):
    """Home page with upload form"""
    form = ImageUploadForm()
    context = {
        'form': form,
        'page_title': 'Image Transcriber - Dr. Apekshya Bhattarai'
    }
    return render(request, 'transcriber/index.html', context)


def upload_image(request):
    """Handle image upload and transcription"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the image
                transcription = form.save(commit=False)
                transcription.save()
                
                # Process the image
                service = TranscriptionService()
                result = service.process_image(
                    transcription.image.path, 
                    capitalization_type='all',
                    custom_prompt=transcription.custom_prompt
                )
                
                if result['success']:
                    transcription.original_text = result['original_text']
                    transcription.formatted_text = result['uppercase_text']
                    transcription.capitalized_text = result['uppercase_text']
                    if result['custom_response']:
                        transcription.custom_response = result['custom_response']
                    transcription.is_processed = True
                    transcription.save()
                    
                    messages.success(request, 'Image transcribed successfully!')
                    return redirect('transcriber:detail', pk=transcription.id)
                else:
                    transcription.error_message = result['error']
                    transcription.save()
                    messages.error(request, f"Transcription failed: {result['error']}")
                    return redirect('transcriber:index')
                    
            except Exception as e:
                messages.error(request, f"Error processing image: {str(e)}")
                return redirect('transcriber:index')
        else:
            messages.error(request, 'Invalid form submission')
            return redirect('transcriber:index')
    
    return redirect('transcriber:index')


def detail(request, pk):
    """Display transcription details"""
    transcription = get_object_or_404(ImageTranscription, pk=pk)
    format_form = TextFormatForm()
    custom_prompt_form = CustomPromptForm()
    
    context = {
        'transcription': transcription,
        'format_form': format_form,
        'custom_prompt_form': custom_prompt_form,
        'page_title': f'Transcription #{pk}'
    }
    return render(request, 'transcriber/detail.html', context)


def reformat_text(request, pk):
    """Reformat text with different capitalization"""
    if request.method == 'POST':
        transcription = get_object_or_404(ImageTranscription, pk=pk)
        
        try:
            data = json.loads(request.body)
            capitalization_type = data.get('capitalization_type', 'all')
            
            if transcription.original_text:
                service = TranscriptionService()
                formatted = service.format_text(
                    transcription.original_text, 
                    capitalization_type
                )
                
                transcription.formatted_text = formatted
                transcription.save()
                
                return JsonResponse({
                    'success': True,
                    'formatted_text': formatted
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No text to reformat'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def process_custom_prompt(request, pk):
    """Process custom prompt for transcribed text"""
    if request.method == 'POST':
        transcription = get_object_or_404(ImageTranscription, pk=pk)
        
        try:
            data = json.loads(request.body)
            custom_prompt = data.get('prompt', '').strip()
            
            if not custom_prompt:
                return JsonResponse({
                    'success': False,
                    'error': 'Please enter a prompt'
                }, status=400)
            
            if transcription.original_text:
                service = TranscriptionService()
                response = service.process_custom_prompt(
                    transcription.original_text,
                    custom_prompt
                )
                
                # Save the custom prompt and response
                transcription.custom_prompt = custom_prompt
                transcription.custom_response = response
                transcription.save()
                
                return JsonResponse({
                    'success': True,
                    'response': response
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No text available to process'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def history(request):
    """Display transcription history"""
    transcriptions_list = ImageTranscription.objects.all()
    paginator = Paginator(transcriptions_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': 'Transcription History'
    }
    return render(request, 'transcriber/history.html', context)


def delete_transcription(request, pk):
    """Delete a transcription"""
    transcription = get_object_or_404(ImageTranscription, pk=pk)
    
    if request.method == 'POST':
        transcription.delete()
        messages.success(request, 'Transcription deleted successfully!')
        return redirect('transcriber:history')
    
    return redirect('transcriber:detail', pk=pk)


@require_http_methods(["GET"])
def api_transcription(request, pk):
    """API endpoint to get transcription data"""
    transcription = get_object_or_404(ImageTranscription, pk=pk)
    
    data = {
        'id': transcription.id,
        'original_text': transcription.original_text,
        'formatted_text': transcription.formatted_text,
        'capitalized_text': transcription.capitalized_text,
        'is_processed': transcription.is_processed,
        'created_at': transcription.created_at.isoformat(),
        'error_message': transcription.error_message
    }
    
    return JsonResponse(data)
