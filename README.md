# wiki2corpus

The application wiki2corpus produces a text corpus from a dump of
Wikipedia.

It's tested on the "enwiki-*-pages-articles-multistream.xml.bz2" files
available from the following URL:

https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia

The goal is to produce a large set of plain-text sentences that can be
processed by automated natural language processing tools. The script
does not produce a complete text-only reproduction of the articles,
although the resulting output is mostly complete.

The output is a set of labeled articles, each of which includes one
sentence per line.


## Limitations

* A few sentences that were in the original article may not be outputted. For example, inadequate processing of the markup can result in something that doesn't look like a sentence, causing it to be filtered out.

* The following pieces of information are not outputted in general: URLs, citations, talk pages, section labels, and lists.

* This script is only tested on Ubuntu 16.04 and it won't run easily outside of a Unix-like environment.


## Prerequisites

The following dependencies are required (these are Ubuntu 16.04
package names):

```
php sed python3 python3-nltk perl

```

The WordNet data from NLTK is required. After installing python3-nltk,
run python3, and type the following commands into the interpreter:

```
>>> import nltk
>>> nltk.download()
```

```


## Running the script

First you should have a dump of Wikipedia available. I'll use the file
enwiki-20170820-pages-articles-multistream.xml.bz2 in the example.

Extract the archive (or clone the repository) into its own directory
and change to the new directory.

You may need to edit the top of file docusplitter.py to point to the
correct programs on your system:

```
PERL_CMD='/usr/bin/perl'
PHP_CMD='/usr/bin/php'
SED_CMD='/bin/sed'
```

The main script to run is docusplitter.py. This script MUST be run
from the same directory where the script and the other files of the
archive are located.

Run the script as follows.

```
./docusplitter.py -xmlbz2 enwiki-20170820-pages-articles-multistream.xml.bz2 > wiki-output.txt
```

This will take a while to finish. The file wiki-output.txt will
contain the uncompressed, plain text output that looks like the
following:


```
** Article: Anarchism
Anarchism is a political philosophy that advocates self-governed societies based on voluntary institutions.

These are often described as stateless societies, although several authors have defined them more specifically as institutions based on non-hierarchical free associations.

Anarchism holds the state to be undesirable, unnecessary, and harmful.
```




## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

However, the included sentence splitter is not covered under this license (the files **HONORIFICS**, **sentence-boundary.pl**, and **README.sentence-boundary**). See **README.sentence-boundary** for license details. This splitter is a modified version of the script by **Marcia Munoz** (http://cogcomp.cs.illinois.edu/software/tools/sentenceboundary.tar.gz).


## Authors

* **Michael Gabilondo** - [mgabilo](https://github.com/mgabilo)
