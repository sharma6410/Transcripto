from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_topic_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_topic(text):
    candidate_labels = [
        "Education", "Finance", "Health", "Entertainment",
        "Politics", "Technology", "Spirituality", "Lifestyle", "Science"
    ]
    classifier = load_topic_classifier()
    result = classifier(text, candidate_labels=candidate_labels)
    top_label = result["labels"][0]
    confidence = result["scores"][0]
    return top_label, confidence
