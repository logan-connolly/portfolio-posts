FROM rocker/r-rmd:latest

# Install linux dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libudunits2-dev \
        gdal-bin \
        libgdal.dev \
        libproj-dev \
        libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R dependencies
RUN install2.r --error \
    extrafont \
    gdtools \
    gridExtra \
    hrbrthemes \
    data.table \
    ggplot2 \
    sf \
    tidytext \
    tm \
    wordcloud

# Copy over files
WORKDIR /render
COPY . .
