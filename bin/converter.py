#!/usr/bin/env python3

def dump_tsv(emoji, pretty=False):
    """ Dump to tsv """
    for k,v in emoji.items():
        print(k, (', '.join(v)), sep="\t")

def dump_json(emoji, pretty=False):
    """ Dump to json """
    import json
    import sys

    if pretty:
        json.dump(emoji, sys.stdout, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        json.dump(emoji, sys.stdout, ensure_ascii=False, sort_keys=True)

def dump_yaml(emoji, pretty=False):
    """ Dump to yaml """
    from ruamel.yaml import YAML

    import sys

    yaml = YAML()
    yaml.allow_unicode = True
    if pretty:
        yaml.indent(sequence=4, offset=2)
    yaml.dump(dict(emoji), sys.stdout)

def parse_args():
    """ Process command line args

    Returns:
        args
    """
    import argparse

    parser = argparse.ArgumentParser(
        description = ('This script converts Unicode CLDR annotation XML '
            'documents (that is, emoji and their descriptors), into more '
            'readily-usable tsv,json, or yaml. Output is sorted at all '
            'levels.'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--format', '-f',
                        type=str,
                        choices={'json', 'yaml', 'tsv'},
                        help=('Format to output.')
                        )
    parser.add_argument('--pretty', '-p',
                        action='store_true',
                        required=False,
                        default=True,
                        help='Pretty print?',
                        )
    parser.add_argument('--failifempty',
                        action='store_true',
                        required=False,
                        default=False,
                        help=('Fail with 1 if the given XML file contains no '
                              'annotations.')
                        )
    parser.add_argument('xmlfiles',
                        nargs='+',
                        help=('Unicode CLDR annotations XML file '
                            'containing emoji and their descriptors.')
                           )
    return parser.parse_args()

def main():
    from collections import defaultdict

    import json
    import sys
    import xmltodict

    args = parse_args()

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

    emoji = defaultdict(set)
    for emojidata in annotations:
        descriptors = emojidata['#text'].split('|')
        descriptors = [elem.strip() for elem in descriptors]
        emoji[emojidata['@cp']].update(descriptors)

    # Convert to dict[list]
    for k,v in dict(emoji).items():
        emoji[k] = sorted(v)

    printers = {
        'tsv': dump_tsv,
        'json': dump_json,
        'yaml': dump_yaml,
    }
    printers[args.format](emoji, args.pretty)


if __name__ == '__main__':
    main()
