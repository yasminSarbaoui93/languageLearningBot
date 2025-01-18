import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.repository.vocabulary import get_all_words, get_or_create_user, extract_learning_language_code


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def llm_response(chat_history: list) -> str | None:
    """
    Function to get the response from OpenAI's language model

    args:
    chat_history: the conversation history array

    returns:
    response: the response from OpenAI's language model
    """

    response = client.chat.completions.create(model="gpt-4o", messages=chat_history)
    return response.choices[0].message.content


def translate_sentence_with_llm(sentence: str, base_language_code: str, additional_system_message = None) -> str | None:
    """
    Function to translate a sentence from a source language to a target language

    args:
    sentence: the sentence to be translated
    source_language: the language code of the source language
    target_language: the language code of the target language

    returns:
    translation: the translated sentence
    """
    if additional_system_message is None:
        additional_system_message = ""
    system_message = f"you are a language translator and all you have you do is respond to the user input message with its exact translation in the following language (code ISO): {base_language_code}. Do not add any additional information in your response, ONLY THE TRANSLATION OF THE USER MESSAGE. Do not eliminate the html commands (e.g. <b> or </b>). {additional_system_message}"
    llm_query=[{"role":"system", "content": system_message}, {"role":"user", "content": sentence}]
    translation = llm_response(llm_query)
    return translation


def text_in_base_language(base_language_code, text, additional_system_message = None):
    """
    Function to translate a text to the base language of the user or return the text if the base language is English

    args:
    text: the text to be translated
    base_language_code: the language code of the base language, ISO 639-1 or ISO 639-2

    returns:
    translation: the translated text
    """
    if base_language_code == "en" or len(base_language_code) < 2:
        return text
    else:
        sentence_in_base_language = translate_sentence_with_llm(text, base_language_code, additional_system_message)
    return sentence_in_base_language