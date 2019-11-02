#!/bin/sh

# Build image 
docker build -t render:rmd .

# Change into post directory
cd $1

# Run container to render html
docker run -it --rm -v${PWD}:/render render:rmd

# Copy output report to readme so that it renders in github
cp ${1}.md readme.md