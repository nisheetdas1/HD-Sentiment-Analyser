# Comment Sentiment Analyzer

A simple Django application that analyzes the sentiment of comments in CSV files using Hugging Face's transformer models.

## Features

- Upload CSV files containing comments
- Automatic detection of comment columns
- Sentiment analysis using pre-trained models
- Visual display of sentiment distribution
- Detailed results with confidence scores

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd SimpleApp
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Usage

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000/
   ```

3. Upload a CSV file with comments:
   - The app works best with files that have a column named "comment"
   - If no such column exists, it will try to detect text columns or use the first column

4. View the sentiment analysis results:
   - See the percentage breakdown of positive vs. negative comments
   - Review each comment with its sentiment classification and confidence score

## CSV Format

The ideal CSV format is simple:

```csv
comment
"This product is excellent! Exactly what I needed."
"Very disappointed with the quality. Will not buy again."
"Average product, nothing special about it."
```

But the app can also handle more complex CSV files with multiple columns. It will try to find the comment column automatically.

## Technical Details

- **Framework**: Django 
- **Front-end**: Bootstrap 5
- **Sentiment Analysis Model**: distilbert-base-uncased-finetuned-sst-2-english (Hugging Face)
- **Data Processing**: Pandas

## Endpoints

The application has two main endpoints:

1. **Home/Upload Endpoint** 
   - URL: `/` (root URL)
   - Methods: GET (displays form) and POST (handles form submission)

2. **Analysis Results Endpoint**
   - URL: `/analyze/<int:file_id>/`
   - Method: GET

## Model Information

The app uses a DistilBERT model fine-tuned on the SST-2 (Stanford Sentiment Treebank) dataset. This model classifies text as either POSITIVE or NEGATIVE. It's a smaller, faster version of BERT that maintains most of the accuracy while being more efficient.

## Requirements

- Python 3.8+
- Django 4.0+
- PyTorch
- Transformers (Hugging Face)
- Pandas

## Customization

To use a different sentiment analysis model, modify the pipeline initialization in `views.py`:

```python
# Example: Change to a multilingual model
sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)
```

## Limitations

- The application classifies sentiment as binary (positive/negative)
- Large CSV files may take longer to process
- The first load may be slow as the model is downloaded and initialized

## License

This project is licensed under the MIT License - see the LICENSE file for details.
