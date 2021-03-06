# wiki2corpus

The application wiki2corpus produces a text corpus from a dump of
Wikipedia.

It's tested on the "enwiki-*-pages-articles-multistream.xml.bz2" files
available from the following URL:

https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia

The goal is to produce a large set of plain-text sentences that can be
processed by automated natural language processing tools.


## Transformations

* Sentences are outputted one per line, using a pre-existing sentence boundary detector that comes packaged

* Some sentences are thrown out, since emphasis is on clean data rather than 100% retrieval

* Most processing of markup is done using regular expressions

* The following pieces of information are not outputted in general: URLs, citations, talk pages, section labels, and lists.

* Articles are labeled 

* URLs are replaced by the word -URL-

* The italics, bold or quotations around single words (pronouns or words in WordNet) are removed; otherwise, the italics, bold or quotations are changed into double quotes

* WikiMedia [[links]] are replaced by plain text

* WikiMedia [[links|substitute text]] are replaced by plain substitute text

* Some HTML such &<i></i>quot; or line break tags are processed, including many &lt;ref&gt; tags, and enclosed referenced sections removed

* WikiMedia [[WikiPedia:Talk]] or [these types of links] replaced by quoted contents

* Post-processing rules throw out sentences with garbage: (1) Sentences with certain non-alphanumeric characters, (2) Sentences with an odd-number of quotations (mismatched), (3) Sentences not starting with an uppercase character and terminating with punctuation




## Prerequisites

This script is only tested on Ubuntu 16.04 and it won't run easily
outside of a Unix-like environment.  The following dependencies are
required (these are Ubuntu 16.04 package names):


```
php sed python3 python3-nltk perl
```

The WordNet data from NLTK is required. After installing python3-nltk,
run python3, and type the following commands into the interpreter:

```
>>> import nltk
>>> nltk.download()
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
contain uncompressed, plain text articles.

Each article is labeled as "** Article: article-name", and is followed
by the sentences in article, one per line. For example, the first bit
of output produced by the script is the following:

```
** Article: Anarchism
Anarchism is a political philosophy that advocates self-governed societies based on voluntary institutions.

These are often described as stateless societies, although several authors have defined them more specifically as institutions based on non-hierarchical free associations.

Anarchism holds the state to be undesirable, unnecessary, and harmful.
```


## License

This project is licensed under the MIT License (see the [LICENSE](LICENSE) file for details), with the following exceptions:

* The files HONORIFICS and sentence-boundary.pl (see [README.sentence-boundary](README.sentence-boundary) for details), which are a modified version of a [program](http://cogcomp.cs.illinois.edu/software/tools/sentenceboundary.tar.gz) by Marcia Munoz.

* The file url.re was taken from code found on blog by Mike Malone which is now [defunct](https://web.archive.org/web/20070509042353/http://immike.net/blog/2007/04/06/5-regular-expressions-every-web-programmer-should-know/)


## Authors

* **Michael Gabilondo** - [mgabilo](https://github.com/mgabilo)

