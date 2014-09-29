#!/bin/bash

# http://stackoverflow.com/a/246128/2193410 (Can a Bash script tell what directory it's stored in?)
SYSASSETS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"
SYSASSETS_MANPAGES_DIR="$SYSASSETS_DIR/man_pages"
MANPAGES_REPO_SRC="http://git.kernel.org/pub/scm/docs/man-pages/man-pages"
MANPAGES_LOCAL_REPO_DIR="$SYSASSETS_MANPAGES_DIR/man-pages"
HTML_DIR="$SYSASSETS_MANPAGES_DIR/html"

echo "Getting latest man page sources..."
# https://gist.github.com/nicferrier/2277987 (Clone a git repo if it does not exist, or pull into it if it does exist)
if [ ! -d $MANPAGES_LOCAL_REPO_DIR/.git ]
then
    git clone $MANPAGES_REPO_SRC $MANPAGES_LOCAL_REPO_DIR
else
    cd $MANPAGES_LOCAL_REPO_DIR
    git pull $MANPAGES_REPO_SRC
fi

echo "Generating HTML files..."
cd $MANPAGES_LOCAL_REPO_DIR
make HTDIR="$HTML_DIR" HTOPTS="-r" html

echo "Generating index.html..."
cd $HTML_DIR
cat > index.html << EOF
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>Man page index</TITLE>
</HEAD>
<BODY>
<h1>Linux Man Pages</h1>
<p>List of man pages by section</p>
<hr />
EOF

# Adapted from http://git.kernel.org/cgit/docs/man-pages/man-pages.git/tree/Makefile#n44
for i in man?; do \
	echo -e "<h3>$i</h3>\n<ul>" >> index.html
	find "$i/" -type f | while read f; do \
		# http://stackoverflow.com/a/19915925/2193410 (In shell, split a portion of a string with dot as delimiter)
		IFS=. read FUNC SECTION EXT <<<"`basename $f`"
		echo "<li><a href=\"$f\">$FUNC ($SECTION)</a></li>" >> index.html
	done; \
	echo "</ul>" >> index.html
done;

cat >> index.html << EOF
<hr />
<p>This index was generated on $(date --utc)</p>
</BODY>
</HTML>
EOF
