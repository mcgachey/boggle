import re
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Removes invalid words from a text file (assuming one word per line)'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str)
        parser.add_argument('output_file', type=str)

    def handle(self, *args, **options):
        in_filename = options['input_file']
        out_filename = options['output_file']
        # TODO: Check file locations exist, correct access, etc
        self.stdout.write(
            u"Scrubbing file {} and writing to {}".format(
                in_filename, out_filename
            )
        )
        ascii_letters = re.compile(r'^([a-zA-Z]+)$')
        with open(in_filename) as in_file:
            with open(out_filename, 'w') as out_file:
                for word in in_file:
                    word = word.strip()
                    if len(word) >= 3 and len(
                            word) <= 16 and ascii_letters.match(word):
                        out_file.write("{}\n".format(word.lower()))
        self.stdout.write(self.style.SUCCESS(
            "Wrote output to {}".format(out_filename))
        )