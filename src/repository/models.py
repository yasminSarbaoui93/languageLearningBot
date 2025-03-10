class User:
    def __init__(self, id: str, name: str, surname: str, username: str,email: str, telegram_id: str, active_dictionary_id: str, partition_key: str = "shared"):
        self.id = id
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.telegram_id = telegram_id
        self.active_dictionary_id = active_dictionary_id #organized by base_language-learning language, eg en-de or by dictionary_id
        self.partition_key = partition_key

class Dictionary:
    def __init__(self, id: str, dictionary_name: str, base_language_code: str, learning_language_code: str, user_id: str):
        self.id = id
        self.dictionary_name = dictionary_name
        self.base_language_code = base_language_code
        self.learning_language_code = learning_language_code
        self.user_id = user_id

class Word:
    def __init__(self, id: str, dictionary_id: str, base_language_code: str, base_language_word: str, learning_language_code: str, learning_language_word: str):
        self.id = id
        self.dictionary_id = dictionary_id
        self.base_language_code = base_language_code
        self.base_language_word = base_language_word
        self.learning_language_code = learning_language_code
        self.learning_language_word = learning_language_word
    