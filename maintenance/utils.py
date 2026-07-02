import os
import sys
from io import BytesIO
from PIL import Image
import fitz  # PyMuPDF
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_image(uploaded_file, max_size_mb=1):
    """
    Compress an uploaded image to be under max_size_mb.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if uploaded_file.size <= max_size_bytes:
        return uploaded_file

    try:
        img = Image.open(uploaded_file)
        
        # Convert to RGB if it's RGBA (for JPEG saving)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        format_to_save = 'JPEG'
        content_type = 'image/jpeg'
        
        quality = 85
        output = BytesIO()
        img.save(output, format=format_to_save, quality=quality, optimize=True)
        
        while output.tell() > max_size_bytes and quality > 20:
            quality -= 10
            output = BytesIO()
            img.save(output, format=format_to_save, quality=quality, optimize=True)
            
        if output.tell() > max_size_bytes:
            # Still too big, scale it down
            width, height = img.size
            img = img.resize((int(width * 0.7), int(height * 0.7)), Image.Resampling.LANCZOS)
            output = BytesIO()
            img.save(output, format=format_to_save, quality=30, optimize=True)
            
        output.seek(0)
        filename = uploaded_file.name
        if not filename.lower().endswith('.jpg') and not filename.lower().endswith('.jpeg'):
            filename = os.path.splitext(filename)[0] + '.jpg'
            
        return InMemoryUploadedFile(
            output,
            'ImageField',
            filename,
            content_type,
            sys.getsizeof(output),
            None
        )
    except Exception as e:
        print(f"Error compressing image: {e}")
        return uploaded_file

def compress_pdf(uploaded_file, max_size_mb=1):
    """
    Compress a PDF using PyMuPDF.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if uploaded_file.size <= max_size_bytes:
        return uploaded_file

    try:
        uploaded_file.seek(0)
        file_bytes = uploaded_file.read()
        
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        output = BytesIO()
        doc.save(output, garbage=4, deflate=True, clean=True)
        doc.close()
        
        output.seek(0)
        return InMemoryUploadedFile(
            output,
            'FileField',
            uploaded_file.name,
            'application/pdf',
            sys.getsizeof(output),
            None
        )
    except Exception as e:
        print(f"Error compressing PDF: {e}")
        return uploaded_file

def compress_file(uploaded_file):
    """
    Determine file type and apply appropriate compression.
    """
    if hasattr(uploaded_file, 'name') and uploaded_file.name:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.webp']:
            return compress_image(uploaded_file)
        elif ext == '.pdf':
            return compress_pdf(uploaded_file)
    return uploaded_file
