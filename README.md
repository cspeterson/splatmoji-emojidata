splatmoji-emojidata
===================

A simple machine- and human-readable complete collection of all emoji, with keywords in all available languages, kept current directly from Unicode releases.

This repository is updated directly from The Unicode Consortium's latest [CLDR] (Common Local Data Repository) which Unicode provides for internationalization in general, but which also happens to provide handy internationalized keywords for emoji.

It is maintained for anyone who needs easily-parsable emoji in one of several formats, and directly for use in my own [Splatmoji], the Linux desktop emoji/emoticon picker.

<img src="assets/logo.png" width="400">

# Installation

Not much to it:

```
git clone https://github.com/cspeterson/splatmoji-emojidata.git
# Now you have the data! 😀
```

# Using the data

## TLDR

If you're just looking for the obvious English-language full emoji collections, those would be either:

* `data/{json,tsv,yaml}/en.all.{json,tsv,yaml}`: the full base set of emoji with English-language annotations.

## How is this data organized?

This repo includes all of the annotated emoji per available language.

The same data is made available in json, tsv, and yaml.

The files are named according to the the source CLDR data files using standard language and locale identifiers, e.g. `en_GB` is "British English," `de_CH` is "Swiss Standard German," etc.

```sh
# A sampling of the data directories
├── data
│   ├── json
│       ├── [...]
│       ├── en.json
│       ├── en_AU.json
│       ├── en_CA.json
│       ├── en_GB.json
│       └── [...]
│   ├── tsv
│       ├── [...]
│       ├── en.tsv
│       ├── en_AU.tsv
│       ├── en_CA.tsv
│       ├── en_GB.tsv
│       └── [...]
│   └── yaml
│       ├── [...]
│       ├── en.yaml
│       ├── en_AU.yaml
│       ├── en_CA.yaml
│       ├── en_GB.yaml
│       └── [...]
```

As for the individual formats, they all contain the same data in as near the same format as possible:

JSON:

```json
{
    "🤓": [
        "face",
        "geek",
        "nerd"
        "nerd face",
    ],
}
```

TSV:

```
🤓      face, geek, nerd, nerd face
```

YAML:

```yaml
🤓:
  - face
  - geek
  - nerd
  - nerd face
```

--------------------------------

# Versioning

The major version of this package is always based on the Unicode CLDR version from which is sourced. The minor and patch versions should follow [Semver 2.0.0] conventions.

# Reproducing the data directly from the source

The repo should be up to date with the latest CLDR from Unicode, but if for some reason you need regenerate the data...

## Requirements

For the python script that does the conversion:

* python 3

For the Bash script that automates the whole process:

* bash
* wget
* unzip

## Setup

If you use virtual environments:

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Or if you don't use virtual environments but should:

```sh
pip3 install -r requirements.txt
```

## Usage

```sh
# With no arguments, this script will fetch and convert directly from the latest CLDR zip and other files:
bin/convert_all_cldr

# If you have a particular version on hand:
bin/convert_all_cldr -c /path/to/cldr/core.zip -s /path/to/emoji-variation-sequences.txt -o /path/to/emoji-ordering-rules.txt
```

--------------------------------

# Contributing

The Unicode Consortium has kind of already done the contributing by making the CLDR data available, but I'm open to any improvements or suggestions. 🙂

# Self-promotion

This repository was created and is maintained by [Christopher Peterson] for use in [Splatmoji].

Also, if you're here you're probably a nerd of some variety and should definitely also check out the awesome podcast [Decipher SciFi] 🤓

# Licenses

CLDR data files included in this repository in the `lib/` directory are distributed under the [Unicode Data License](lib/unicode-license.txt).

The rest of the code and data in this repository are distributed under the [Apache license](LICENSE.md) 

[CLDR]: http://cldr.unicode.org/index/downloads
[Christopher Peterson]: https://chrispeterson.info
[Decipher SciFi]: https://decipherscifi.com
[Semver 2.0.0]: https://semver.org/
[Splatmoji]: https://github.com/cspeterson/splatmoji
