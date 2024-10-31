import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()
language_key = os.getenv("LANGUAGESTUDIO_KEY")
language_endpoint = os.getenv("LANGUAGESTUDIO_ENDPOINT")


# Function to authenticate the client to use the Azure Text Analytics API
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()
#Function to detect language code of source text and translation
def detect_language_code(text):
    language_code = client.detect_language([text])[0].primary_language.iso6391_name
    return language_code
