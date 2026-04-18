import base64
import json
from pathlib import Path
from django.conf import settings
import openai
import re


class TranscriptionService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    def encode_image_to_base64(self, image_path):
        """Encode image file to base64 string"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.standard_b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            raise Exception(f"Error encoding image: {str(e)}")

    def transcribe_image(self, image_path):
        """Transcribe text from image using OpenAI Vision API"""
        try:
            # Check file size and extension
            path = Path(image_path)
            if not path.exists():
                raise Exception("Image file not found")

            # Determine image media type
            media_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            
            file_ext = path.suffix.lower()
            if file_ext not in media_type_map:
                raise Exception(f"Unsupported image format: {file_ext}")
            
            media_type = media_type_map[file_ext]

            # Encode image to base64
            base64_image = self.encode_image_to_base64(image_path)

            # Call OpenAI Vision API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": "Please transcribe all the text you can see in this image. Provide accurate text transcription without any modifications."
                            }
                        ],
                    }
                ],
            )

            # Extract transcribed text
            transcribed_text = response.content[0].text
            return transcribed_text

        except openai.APIError as e:
            raise Exception(f"OpenAI API Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Transcription Error: {str(e)}")

    def format_text_to_uppercase(self, text):
        """Convert text to uppercase"""
        return text.upper()

    def format_text_to_title_case(self, text):
        """Convert text to title case"""
        return text.title()

    def format_text_to_sentence_case(self, text):
        """Convert text to sentence case"""
        sentences = re.split(r'([.!?]+)', text)
        formatted_sentences = []
        
        for i, sentence in enumerate(sentences):
            if i % 2 == 0 and sentence.strip():
                # This is a sentence part
                sentence = sentence.strip()
                if sentence:
                    formatted_sentences.append(sentence[0].upper() + sentence[1:].lower())
            else:
                # This is punctuation
                formatted_sentences.append(sentence)
        
        return ' '.join(formatted_sentences)

    def format_text(self, text, capitalization_type='all'):
        """
        Format text based on capitalization type
        
        Args:
            text: The text to format
            capitalization_type: 'all', 'title', or 'sentence'
        
        Returns:
            Formatted text
        """
        if not text:
            return ""
        
        # Clean up text
        text = text.strip()
        
        if capitalization_type == 'all':
            return self.format_text_to_uppercase(text)
        elif capitalization_type == 'title':
            return self.format_text_to_title_case(text)
        elif capitalization_type == 'sentence':
            return self.format_text_to_sentence_case(text)
        else:
            return self.format_text_to_uppercase(text)  # Default to uppercase

    def process_custom_prompt(self, text, prompt):
        """
        Process transcribed text with a custom prompt/instruction
        
        Args:
            text: The transcribed text
            prompt: Custom instruction or question
        
        Returns:
            Response from OpenAI based on the custom prompt
        """
        try:
            if not text or not prompt:
                return None
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": f"Here is some transcribed text:\n\n{text}\n\nPlease do the following:\n{prompt}"
                    }
                ],
            )
            
            return response.content[0].text
        
        except openai.APIError as e:
            raise Exception(f"OpenAI API Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing prompt: {str(e)}")

    def process_image(self, image_path, capitalization_type='all', custom_prompt=None):
        """
        Complete pipeline: transcribe image and format text
        
        Args:
            image_path: Path to the image file
            capitalization_type: How to capitalize the text
            custom_prompt: Optional custom instruction for the transcribed text
        
        Returns:
            Dictionary with original and formatted text
        """
        try:
            # Transcribe image
            original_text = self.transcribe_image(image_path)
            
            # Format text
            formatted_text = self.format_text(original_text, capitalization_type)
            
            # Also provide uppercase version
            uppercase_text = self.format_text_to_uppercase(original_text)
            
            # Process custom prompt if provided
            custom_response = None
            if custom_prompt:
                custom_response = self.process_custom_prompt(original_text, custom_prompt)
            
            return {
                'success': True,
                'original_text': original_text,
                'formatted_text': formatted_text,
                'uppercase_text': uppercase_text,
                'custom_response': custom_response,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'original_text': None,
                'formatted_text': None,
                'uppercase_text': None,
                'custom_response': None,
                'error': str(e)
            }
