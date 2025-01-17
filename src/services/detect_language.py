import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


load_dotenv()
language_key = os.getenv("LANGUAGESTUDIO_KEY")
language_endpoint = os.getenv("LANGUAGESTUDIO_ENDPOINT")


def authenticate_client() -> TextAnalyticsClient:
    """
    Function to authenticate the client to use the Azure Text Analytics API
    
    returns:
    text_analytics_client: the client object to use the API
    """
    if not language_endpoint:
        raise ValueError("LANGUAGESTUDIO_ENDPOINT is not set")
    ta_credential = AzureKeyCredential(language_key)# type: ignore
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint,
            credential=ta_credential)
    return text_analytics_client


client = authenticate_client()
def detect_language_code(text) -> str:
    """
    Function to detect the language code of a given text
    
    args:
    text: the text to detect the language code for
    
    returns:
    language_code: the language code of the text (e.g. en, de, fr)
    """
    language_code = client.detect_language([text])[0].primary_language.iso6391_name
    return language_code