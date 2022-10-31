from django.test import TestCase

from newscraper.top_15_words.map_reduce import map_string, reduce


class TestMapReduce(TestCase):

    def setUp(self):
        self.sentence = 'Danas je divan dan dan'

    def test_map(self):
        map_obj = map_string(self.sentence)
        counter = 0
        for obj in map_obj:
            counter += 1

        self.assertEqual(counter, 5)

    def test_reduce(self):
        map_obj = map_string(self.sentence)

        results = reduce(map_obj)

        print(results)

        self.assertEqual(results.get('dan'), 2)
