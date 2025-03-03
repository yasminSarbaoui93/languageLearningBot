class User:
    def __init__(self, id: str, name: str, surname: str, username: str,email: str, base_language: str, learning_language: str, telegram_id: str, active_dictionary: str, partition_key: str = "shared"):
        self.id = id
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.base_language = base_language
        self.learning_language = learning_language
        self.telegram_id = telegram_id
        self.active_dictionary = active_dictionary
        self.partition_key = partition_key

class Dictionary:
    def __init__(self, id: str, base_language_code: str, learning_language_code: str, partition_key: str):
        self.id = id
        self.base_language_code = base_language_code
        self.learning_language_code = learning_language_code
        self.partition_key = partition_key

class Word:
    def __init__(self, id: str, user_id: str, language_code: str, text: str, translation_text: str, translation_language_code: str):
        self.id = id
        self.user_id = user_id
        self.language_code = language_code
        self.text = text
        self.translation = {
            "text": translation_text,
            "language_code": translation_language_code
        }