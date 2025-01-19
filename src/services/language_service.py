import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import pycountry
from pycountry import languages

load_dotenv()
language_key = os.getenv("LANGUAGESTUDIO_KEY")
language_endpoint = os.getenv("LANGUAGESTUDIO_ENDPOINT")


def _authenticate_client() -> TextAnalyticsClient:
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


def detect_language_code(text) -> str:
    """
    Function to detect the language code of a given text
    
    args:
    text: the text to detect the language code for
    
    returns:
    language_code: the language code of the text (e.g. en, de, fr)
    """
    client = _authenticate_client()
    language_code = client.detect_language([text])[0].primary_language.iso6391_name
    return language_code

def language_name_from_code(language_code) -> str:
    """
    Function to get the language name from the language code
    
    args:
    language_code: the language code to get the language name for
    
    returns:
    language_name: the language name of the language code
    """
    try:
        language = pycountry.languages.get(alpha_2=language_code)
        language_name = language.name
        return language_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""