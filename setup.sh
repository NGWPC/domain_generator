#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Setting up R environment for domain_generator/hfsubsetR"

echo "Updating package lists and installing system dependencies"
sudo apt update

echo "Installing R packages"
sudo apt install -y \
    r-cran-sf \
    r-cran-terra \
    r-cran-collapse \
    r-cran-data.table \
    r-cran-dbi \
    r-cran-dplyr \
    r-cran-dbplyr \
    r-cran-tidyr \
    r-cran-plumber \
    r-cran-logger \
    r-cran-cachem \
    r-cran-jsonlite \
    r-cran-rlang \
    r-cran-remotes \
    r-cran-rcpp \
    r-cran-bh

echo "Configuring R package repository for Ubuntu 22.04"
echo 'options(repos = c(CRAN = "https://packagemanager.posit.co/cran/__linux__/jammy/latest"))' > ~/.Rprofile

echo "Installing additional R dependencies or hfsubsetR"
sudo Rscript -e 'install.packages("arrow", repos = c("https://apache.r-universe.dev", "https://cloud.r-project.org"))'
sudo Rscript -e 'install.packages("qs")'
sudo Rscript -e 'remotes::install_github("mikejohnson51/zonal")'
sudo Rscript -e 'remotes::install_github("NGWPC/hfsubsetR")'

echo "R environment setup complete!"
echo "To verify installation, run: R --version"
