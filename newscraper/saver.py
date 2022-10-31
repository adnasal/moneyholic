from newscraper.models import Wordcount


def save_to_db(reduced_map):
    for current_word, current_count in reduced_map.items():

        try:
            existing = Wordcount.objects.get(word=current_word)
        except Wordcount.DoesNotExist:
            Wordcount.objects.create(word=current_word, count=current_count)
            return

        existing.count += current_count
        existing.save()
