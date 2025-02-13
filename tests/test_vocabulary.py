import unittest

from repository.vocabulary import get_or_create_user_id

class VocabularyTests(unittest.TestCase):

    def test_upper(self):
        get_or_create_user_id("1234567890", "testuser", "Test", "User")

        self.assertEqual('foo'.upper(), 'FOO')    

if __name__ == '__main__':
    unittest.main()
