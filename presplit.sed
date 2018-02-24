# 2008, 2009, 2018 Michael Gabilondo

# remove headings
s=\=\=+([^=]+)\=\=+==g

# breaks and paragraph html tags are newlines
s=<br>=\n=g
s=<br />=\n=g
s=<p>=\n=g

# html substitutions
s=&quot;="=g
s=&amp;=&=g
s=&nbsp;= =g
s=&ndash;=-=g
s=&mdash;=--=g
s=&lt;=<=g
s=&gt;=>=g

# italics are often used for titles
s='''''="=g

# bold goes to nothing
s='''==g

# italics are often used for titles
s=''="=g

# [[WikiPedia:Talk|talk]] -> talk
s=\[\[\S+:[^]]+\|([^]|]+)\]\]=\1=g


# [[WikiPedia:Talk]] -> "WikiPedia:Talk"
s=\[\[(\S+:[^]]+)\]\]="\1"=g

# {{Unicode|some text}} -> some text
s=\{\{Unicode\|([^}]+)\}\}=\1=g

# {convert|number|units|...}} -> number units
s=\{\{convert\|([^}|]+)\|([^}|]+)(\|([^}]+))?\}\}=\1 \2=g

# [[SomeArticle|some text]] -> some text
s=\[\[([^]|]+)\|([^]|]+)\]\]=\2=g

# [[some text]] -> some text
s=\[\[([^]|]+)\]\]=\1=g

# remove references
s=<ref([^<>]*)\/>==g
s=<ref([^<>]*)>[^<]+</ref>==g

# {{stuff}} -> 
s=\{\{[^}]+\}\}==g

# [URL] ->      (citation)
s=\[-URL-\]==g

# [URL some text here] -> some text here
s=\[-URL- ([^]|]+)\]=\1=g

# make colons periods and newlines; colons are also used for wikimarkup
#s=:+=\.\n=g

# "stuff." -> "stuff".
s=\.\"=\"\.=g

# "stuff," -> "stuff",
s=\,\"=\"\,=g

# again
s=<ref([^<>]*)>[^<]+</ref>==g

# single line comments
s=<!--([^<>]*)-->==g

