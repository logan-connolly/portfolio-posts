#!/bin/sh

# Build image 
docker build -t rmd:german-election .

# Run container to render html
docker run -it --rm -v${PWD}:/render rmd:german-election

# Remove image
while getopts "d" OPTION
do
        case $OPTION in
                d)
                        docker rmi -f rmd:german-election
                        exit
                        ;;
        esac
done