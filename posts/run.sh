#!/bin/sh

# Build image 
docker build -t $2 $1

# Run container to render html
docker run -it --rm -v${PWD}:/render $2

# Copy report to readme so that it renders in github
cp $1/$1.md $1/readme.md

# Remove image
while getopts "d" OPTION
do
        case $OPTION in
                d)
                        docker rmi -f $2
                        exit
                        ;;
        esac
done