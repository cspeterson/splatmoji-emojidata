#!/usr/bin/env python3

def dump_tsv(emoji, pretty=False):
    """ Dump list of emoji from key:val pairs to tsv """
    for k,v in emoji:
        print(k, (', '.join(v)), sep="\t")

def dump_json(emoji, pretty=False):
    """ Dump list of emoji from key:val pairs to json """
    from collections import OrderedDict

    import json
    import sys

    emoji = OrderedDict(emoji)
    if pretty:
        json.dump(emoji, sys.stdout, ensure_ascii=False, indent=4, separators=(',', ': '))
    else:
        json.dump(emoji, sys.stdout, ensure_ascii=False)

def dump_yaml(emoji, pretty=False):
    """ Dump list of emoji from key:val pairs to dict to yaml """
    from collections import OrderedDict
    from ruamel.yaml import YAML

    import sys

    emoji = OrderedDict(emoji)

    yaml = YAML()
    yaml.allow_unicode = True
    if pretty:
        yaml.indent(sequence=4, offset=2)
    yaml.dump(dict(emoji), sys.stdout)

def parse_args():
    """ Process command line args """
    import argparse

    parser = argparse.ArgumentParser(
        description = (
            'This script converts Unicode CLDR annotation XML '
            'documents (that is, emoji and their descriptors), into more '
            'readily-usable tsv,json, or yaml. Output is sorted at all '
            'levels.'
            ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices={'json', 'yaml', 'tsv'},
        help=('Format to output.')
    )
    parser.add_argument(
        '--pretty', '-p',
        action='store_true',
        required=False,
        default=True,
        help='Pretty print?',
    )
    parser.add_argument(
        '--failifempty',
        action='store_true',
        required=False,
        default=False,
        help='Fail with 1 if the given XML file contains no annotations.'
    )
    parser.add_argument(
        '--ordering-rules', '-o',
        dest='ordering_file',
        type=str,
        required=True,
        default=None,
        help=(
            '`emoji-ordering-rules.txt` from Unicode data (this should be '
            'from the Unicode data version matching the CLDR release being '
            'used).Providing this ensures results are sorted not by value '
            'order but by the sensible grouped order provided by Unicode to '
            'organize related emoji together.')
    )
    parser.add_argument(
        '--presentation-sequences',
        dest='sequences_file',
        required=True,
        default=None,
        type=str,
        help=(
            '`emoji-variation-sequences.txt` from Unicode data (this should be '
            'from the Unicode data version matching the CLDR release being '
            'used).Providing this ensures that any older emoji that can also '
            'be "presented" as text are specifically presented as emoji. '
            'Ex: ☎️  vs ☎ '
            )
    )
    parser.add_argument(
        'xmlfiles',
        nargs='+',
        help=(
            'Unicode CLDR annotations XML files containing emoji and their '
            'descriptors.'
            )
    )
    return parser.parse_args()

def main():
    from collections import defaultdict, OrderedDict
    from functools import cmp_to_key
    from icu import RuleBasedCollator

    import json
    import os
    import re
    import sys
    import xmltodict

    args = parse_args()
    script_dir = os.path.dirname(os.path.realpath(__file__))

    annotations = []
    for xmlfile in args.xmlfiles:
        with open(xmlfile, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read())
        try:
            annotations.extend(doc['ldml']['annotations']['annotation'])
        except KeyError:
            print("File {} included no annotations. Exiting.".format(xmlfile), file=sys.stderr)
            if args.failifempty:
                sys.exit(1)
            else:
                sys.exit(0)

    # Parse out emoji and a list of their unique descriptors
    emoji = defaultdict(set)
    for emojidata in annotations:
        descriptors = emojidata['#text'].split('|')
        descriptors = [elem.strip() for elem in descriptors]
        emoji[emojidata['@cp']].update(descriptors)

    if not args.sequences_file:
        args.sequences_file = os.path.join(script_dir, 'lib', 'emoji-variation-sequences.txt')
    # Replace all old text representations
    # listed by unicode with their emoji representation equivalent
    # Depending on the font, these representations can often differ.
    with open(args.sequences_file) as f:
        for line in f:
            line = line.strip()
            emojipatt = (
                r'^(?P<char1>[0-9A-F]+)'
                r'\s(?P<char2>[0-9A-F]+)'
                r'\s+;\s+emoji style;\s+#\s+\([\.0-9]+\)\s+'
                r'(?P<desc>[ A-Z]+)$'
                )
            match = re.match(emojipatt, line)
            if match:
                oldchar_escaped = r'\U{0:0>8}'.format(match.group('char1'))
                newchar_escaped = r'\U{0:0>8}\U{1:0>8}'.format(match.group('char1'), match.group('char2'))
                oldchar = oldchar_escaped.encode('utf-8').decode('unicode_escape')
                newchar = newchar_escaped.encode('utf-8').decode('unicode_escape')

                # Replace the old value with the emoji representation
                if oldchar in emoji.keys():
                    emoji[newchar] = emoji[oldchar]
                    del emoji[oldchar]

    # Sort keywords
    emoji = {k:sorted(v) for (k,v) in emoji.items()}
    emoji = list(emoji.items())

    # Collation/ordering
    # Emoji should not sort by their actual values but by their corresponding
    # collation rules and for this we use the icu library
    if not args.ordering_file:
        args.ordering_file = os.path.join(script_dir, 'lib', 'emoji-ordering.txt')
    with open(args.ordering_file, encoding='utf-8') as fd:
        doc = xmltodict.parse(fd.read())
    try:
        ordering_lines = doc['collation']['cr'].splitlines()
    except KeyError:
        print('Emoji Ordering file {} included did not include data in '
              'expected format. Exiting.'.format(
                  args.ordering_file,
                  file=sys.stderr
                  )
            )
        sys.exit(1)
    # The RuleBasedCollator wants its rules as a single string where unquoted
    # whitespace is meaningless, so just join up
    ordering_lines = [l for l in ordering_lines if l[0] != '#']
    ordering = ' '.join(ordering_lines)
    coll = RuleBasedCollator(ordering)

    # Awkwardly sort with a custom old-style comp function becayse the icu
    # python bindings are undocumented and I don't think there is a modern
    # key-style option.
    # And awkwardly address the skin tones so that they wind up on the back of the
    # list instead of the front, as the icu collation ignores them :/.
    def compare_emoji(a, b):
        skin_tones = ['🏻', '🏼', '🏽', '🏾', '🏿']
        if a[0] in skin_tones and not b[0] in skin_tones:
            return 1
        elif b[0] in skin_tones and a[0] not in skin_tones:
            return -1
        elif a[0] in skin_tones and b[0] in skin_tones:
            if a[0] < b[0]:
                return -1
            elif a[0] == b[0]:
                return 0
            else:
                return 1
        else:
            return coll.compare(a[0], b[0])
    emoji = sorted(emoji, key=cmp_to_key(compare_emoji))

    # Dump!
    printers = {
        'tsv': dump_tsv,
        'json': dump_json,
        'yaml': dump_yaml,
    }
    printers[args.format](emoji, args.pretty)


if __name__ == '__main__':
    main()
