# summarizer.py

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Load model and tokenizer once
def load_summarizer(model_name="facebook/bart-large-cnn"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    return summarizer

# Summarize text using the selected model
def summarize_text(text, summarizer, max_chunk=1000):
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summaries = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
        summaries.append(summary)

    return summaries
