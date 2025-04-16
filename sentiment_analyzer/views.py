from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CSVUploadForm
from .models import CSVFile
import pandas as pd
import os
from transformers import pipeline

# Initialize the sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def home(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.save()
            return redirect('analyze', file_id=csv_file.id)
    else:
        form = CSVUploadForm()
    
    return render(request, 'sentiment_analyzer/home.html', {'form': form})

def analyze(request, file_id):
    csv_file = CSVFile.objects.get(id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(csv_file.file))
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Find comment column or use the first column
    comment_column = None
    for col in df.columns:
        if 'comment' in col.lower():
            comment_column = col
            break
    
    if not comment_column and len(df.columns) > 0:
        comment_column = df.columns[0]
    
    if not comment_column:
        return render(request, 'sentiment_analyzer/error.html', 
                     {'error': 'No comment column found in the CSV file'})
    
    # Get the comments
    comments = df[comment_column].astype(str).tolist()
    
    # Perform sentiment analysis in batches to avoid memory issues
    batch_size = 8
    results = []
    
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i+batch_size]
        batch_results = sentiment_analyzer(batch)
        results.extend(batch_results)
    
    # Create result data
    analysis_results = []
    for i, (comment, result) in enumerate(zip(comments, results)):
        # Add row index and truncate long comments for display
        display_comment = comment if len(comment) < 100 else comment[:97] + '...'
        analysis_results.append({
            'row_index': i + 1,
            'comment': display_comment,
            'sentiment': result['label'],
            'score': f"{result['score']:.4f}"
        })
    
    # Calculate summary statistics
    positive_count = sum(1 for result in results if result['label'] == 'POSITIVE')
    negative_count = len(results) - positive_count
    
    # Calculate percentages
    if len(results) > 0:
        positive_percentage = (positive_count / len(results)) * 100
        negative_percentage = (negative_count / len(results)) * 100
    else:
        positive_percentage = negative_percentage = 0
    
    context = {
        'file_name': os.path.basename(file_path),
        'comment_column': comment_column,
        'total_comments': len(comments),
        'positive_count': positive_count,
        'negative_count': negative_count,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'results': analysis_results
    }
    
    return render(request, 'sentiment_analyzer/results.html', context)
