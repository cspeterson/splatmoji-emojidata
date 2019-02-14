splatmoji-emojidata
===================

A simple machine- and human-readable complete collection of all emoji, kept current directly from Unicode releases.

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

* `data/{json,tsv,yaml}/en.base.{json,tsv,yaml}`: the full base set of emoji with English-language annotations.
* `data/{json,tsv,yaml}/en.all.{json,tsv,yaml}`: the full base set of emoji with English-language annotations, *and* all derivations. This is the most comprehensive and includes all skin color variations and country flags.

## How is this data organized?

This repo includes all of the base annotated emoji, the derived emoji variants, and both of the former per available language combined.

The same data is made available in json, tsv, and yaml.

The files are named according to the the source CLDR data files using standard language and locale identifiers, e.g. `en_GB` is "British English," `de_CH` is "Swiss Standard German," etc.

```sh
# A sampling of the data directories
├── data
│   ├── json
│       ├── [...]
│       ├── en.all.json
│       ├── en_AU.all.json
│       ├── en_AU.base.json
│       ├── en_AU.derived.json
│       ├── en.base.json
│       ├── en_CA.all.json
│       ├── en_CA.base.json
│       ├── en_CA.derived.json
│       ├── en.derived.json
│       ├── en_GB.all.json
│       ├── en_GB.base.json
│       ├── en_GB.derived.json
│       └── [...]
│   ├── tsv
│       ├── [...]
│       ├── en.all.tsv
│       ├── en_AU.all.tsv
│       ├── en_AU.base.tsv
│       ├── en_AU.derived.tsv
│       ├── en.base.tsv
│       ├── en_CA.all.tsv
│       ├── en_CA.base.tsv
│       ├── en_CA.derived.tsv
│       ├── en.derived.tsv
│       ├── en_GB.all.tsv
│       ├── en_GB.base.tsv
│       ├── en_GB.derived.tsv
│       └── [...]
│   └── yaml
│       ├── [...]
│       ├── en.all.yaml
│       ├── en_AU.all.yaml
│       ├── en_AU.base.yaml
│       ├── en_AU.derived.yaml
│       ├── en.base.yaml
│       ├── en_CA.all.yaml
│       ├── en_CA.base.yaml
│       ├── en_CA.derived.yaml
│       ├── en.derived.yaml
│       ├── en_GB.all.yaml
│       ├── en_GB.base.yaml
│       ├── en_GB.derived.yaml
│       └── [...]
```

As for the individual formats, they all contain the same data in as near the same format as possible:

JSON:

```json
{
    "🤓": [
        "face",
        "geek",
        "nerd face",
        "nerd"
    ],
}
```

TSV:

```
🤓      face, geek, nerd face, nerd
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
# With no arguments, this script will fetch and convert directly from the latest CLDR zip:
bin/convert_all_cldr

# If you have the zip on hand already
bin/convert_all_cldr /path/to/cldr/core.zip
```

--------------------------------

# Contributing

The Unicode Consortium has kind of already done the contributing by making the CLDR data available, but I'm open to any process improvements or suggestions. 🙂

# Self-promotion

This repository was created and is maintained by [Christopher Peterson] for use in [Splatmoji].

# License

This repository is distributed under the [MIT license](LICENSE.md).

[CLDR]: http://cldr.unicode.org/index/downloads
[Christopher Peterson]: https://chrispeterson.info
[Splatmoji]: https://github.com/cspeterson/splatmoji
