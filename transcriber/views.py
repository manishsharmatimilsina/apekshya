from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
import json
from pathlib import Path

from .models import ImageTranscription, TranscriptionImage
from .forms import ImageUploadForm, TextFormatForm, CustomPromptForm
from .services import TranscriptionService


def register(request):
    """Register a new user"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('transcriber:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'page_title': 'Register'
    }
    return render(request, 'transcriber/register.html', context)


@login_required
def index(request):
    """Home page with upload form"""
    form = ImageUploadForm()
    context = {
        'form': form,
        'page_title': 'Image Transcriber - Dr. Apekshya Bhattarai'
    }
    return render(request, 'transcriber/index.html', context)


@login_required
def upload_image(request):
    """Handle multiple image uploads and transcription"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Get uploaded files and custom prompt
                files = request.FILES.getlist('images')
                custom_prompt = form.cleaned_data.get('custom_prompt', '').strip()

                if not files:
                    messages.error(request, 'Please select at least one image')
                    return redirect('transcriber:index')

                # Create transcription batch
                transcription = ImageTranscription(
                    user=request.user,
                    custom_prompt=custom_prompt if custom_prompt else None
                )
                transcription.save()

                # Process each image
                service = TranscriptionService()
                all_texts = []
                error_occurred = False

                for page_num, file in enumerate(files, 1):
                    try:
                        # Save TranscriptionImage
                        trans_image = TranscriptionImage(
                            transcription=transcription,
                            page_number=page_num
                        )
                        trans_image.image.save(file.name, file, save=True)

                        # Process the image
                        result = service.process_image(
                            trans_image.image.path,
                            capitalization_type='all',
                            custom_prompt=None
                        )

                        if result['success']:
                            trans_image.individual_text = result['original_text']
                            trans_image.save()
                            all_texts.append(f"--- Image {page_num} ---\n\n{result['original_text']}")
                        else:
                            error_occurred = True
                            all_texts.append(f"--- Image {page_num} ---\n\n[Error: {result['error']}]")

                    except Exception as e:
                        error_occurred = True
                        all_texts.append(f"--- Image {page_num} ---\n\n[Error processing image: {str(e)}]")

                # Combine all texts
                combined_text = "\n\n".join(all_texts)

                # Format combined text
                formatted_text = service.format_text(combined_text, 'all')

                # Save transcription
                transcription.original_text = combined_text
                transcription.formatted_text = combined_text
                transcription.capitalized_text = formatted_text

                # Process custom prompt on combined text if provided
                if custom_prompt:
                    custom_response = service.process_custom_prompt(combined_text, custom_prompt)
                    transcription.custom_response = custom_response

                if not error_occurred:
                    transcription.is_processed = True
                    messages.success(request, f'Successfully transcribed {len(files)} image(s)!')
                else:
                    transcription.error_message = 'Some images failed to process'
                    messages.warning(request, 'Some images failed to process but results are available')

                transcription.save()
                return redirect('transcriber:detail', pk=transcription.id)

            except Exception as e:
                messages.error(request, f"Error processing images: {str(e)}")
                return redirect('transcriber:index')
        else:
            messages.error(request, 'Invalid form submission')
            return redirect('transcriber:index')

    return redirect('transcriber:index')


@login_required
def detail(request, pk):
    """Display transcription details"""
    transcription = get_object_or_404(ImageTranscription, pk=pk, user=request.user)
    format_form = TextFormatForm()
    custom_prompt_form = CustomPromptForm()
    
    context = {
        'transcription': transcription,
        'format_form': format_form,
        'custom_prompt_form': custom_prompt_form,
        'page_title': f'Transcription #{pk}'
    }
    return render(request, 'transcriber/detail.html', context)


@login_required
def reformat_text(request, pk):
    """Reformat text with different capitalization"""
    if request.method == 'POST':
        transcription = get_object_or_404(ImageTranscription, pk=pk, user=request.user)
        
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


@login_required
def process_custom_prompt(request, pk):
    """Process custom prompt for transcribed text"""
    if request.method == 'POST':
        transcription = get_object_or_404(ImageTranscription, pk=pk, user=request.user)
        
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


@login_required
def history(request):
    """Display transcription history"""
    transcriptions_list = ImageTranscription.objects.filter(user=request.user)
    paginator = Paginator(transcriptions_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': 'Transcription History'
    }
    return render(request, 'transcriber/history.html', context)


@login_required
def delete_transcription(request, pk):
    """Delete a transcription"""
    transcription = get_object_or_404(ImageTranscription, pk=pk, user=request.user)

    if request.method == 'POST':
        transcription.delete()
        messages.success(request, 'Transcription deleted successfully!')
        return redirect('transcriber:history')

    return redirect('transcriber:detail', pk=pk)


@login_required
@require_http_methods(["GET"])
def api_transcription(request, pk):
    """API endpoint to get transcription data"""
    transcription = get_object_or_404(ImageTranscription, pk=pk, user=request.user)
    
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
