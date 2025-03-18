FROM debian:12.8-slim

ENV LIBARROW_BUILD=false
ENV LIBARROW_MINIMAL=false
ENV NOT_CRAN=true

RUN apt-get update -y && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    libssl-dev \
    libcurl4-openssl-dev \
    r-base \
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

RUN curl -LsSf https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.cargo/bin:${PATH}"

RUN mkdir -p /api/data

COPY ./data/conus_nextgen.gpkg /api/data/

RUN echo 'options(repos = c(CRAN = "https://packagemanager.posit.co/cran/__linux__/bookworm/latest"))' > ~/.Rprofile

RUN Rscript -e 'install.packages("arrow", repos = c("https://apache.r-universe.dev", "https://cloud.r-project.org"))'
RUN Rscript -e 'install.packages("qs")'
RUN Rscript -e 'remotes::install_github("mikejohnson51/zonal")'
RUN Rscript -e 'remotes::install_github("NGWPC/hfsubsetR")'
RUN Rscript -e 'install.packages("logger")'

COPY . /api

WORKDIR /api

RUN uv venv
RUN source .venv/bin/activate
RUN uv pip install -e .

RUN chmod +x /api/entrypoint.sh

CMD ["tail", "-f", "/dev/null"]
