import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
#from detect_language import detect_language_code
from services.language_service import detect_language_code

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


def translate_to_language(base_language_code, text, additional_system_message = None) -> str | None:
    """
    Function to translate a text to the base language of the user or return the text if the base language is English

    args:
    text: the text to be translated
    base_language_code: the language code of the base language, ISO 639-1 or ISO 639-2

    returns:
    translation: the translated text
    """
    if base_language_code == "en" and detect_language_code(text)=="en" or len(base_language_code) < 2:     
        return text
    else:
        sentence_in_base_language = translate_sentence_with_llm(text, base_language_code, additional_system_message)
    return sentence_in_base_language


def extracat_language_code_with_llm(user_input: str) -> str | None:
    """
    Function to extract the language code from the user message. the user message should be the name of the language they want to learn, e.g. spanish, arabo, italiano, frances, etc. 
    given the user input the llm should respond either with a language code in format ISO 639-1 or ISO 639-2, e.g. 'es' for spanish, 'ar' for arabic, 'it' for italian, 'fr' for french, etc., or respond  with error message, informing the user tbat tbere was a mistake
    then create an if else. if the result from the llm is a language code, then you can go on with the conversation and ask the user for the base language. if the result is an error message, then you should ask the user to repeat the language they want to learn
        
    args:
    user_message: the message object from the user

    returns:
    language_code: the language code of the language from user_input

    """
    system_message = "We ask information about what language the user in interested in, and given the user input, you will have to extract in lower case the language code of the language selected by the user (NOT THE LANGUAGE CODE THAT THE USER IS TYPING IN!!). For example, if the user says 'English', you have to respond 'en', if the user says 'inglese', you have to respond 'en', if the user says 'spagnolo', you have to respond 'es'. In case the user message is not containing infromation around a language (for example they wrote a random word or sentence unrelated), respond with 'None'"
    messages = []
    messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": user_input})
    learning_language_code = llm_response(messages)
    if learning_language_code == "None":
        return None
    return learning_language_code

def check_word_typos(word: str, language_code: str) -> str | None:
    """
    Function to check if a word is spelled correctly in a given language

    args:
    word: the word to be checked
    language_code: the language code of the language of the word

    returns:
    corrected_word: the corrected word if it was spelled incorrectly
    """
    system_message = f"you are a language grammatic checker and all you have you do check if the given word or set of words have typos. Do not eliminate the html commands (e.g. <b> or </b>). Do not change for any reason the format (e.g. if the user uses some capital letters, you should keep them or if there are any special characters as / or - or any other). Simply respond with the exact same input but with no typos in case you find any, or respond with the exact input in case there are no typos. The language code of the text is {language_code}."
    messages = []
    messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": word})
    corrected_word = llm_response(messages)
    return corrected_word