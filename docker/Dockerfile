FROM debian:12.8-slim

ENV LIBARROW_BUILD=false
ENV LIBARROW_MINIMAL=false
ENV NOT_CRAN=true
ENV PYTHONPATH=/api:$PYTHONPATH
ENV VENV_PATH=/opt/venv
ENV UV_VENV_PATH=/opt/uv_venv

RUN apt-get update -y && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    python3-full \ 
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
    

RUN python3 -m venv $UV_VENV_PATH
RUN $UV_VENV_PATH/bin/pip install uv
ENV PATH="$UV_VENV_PATH/bin:${PATH}"

RUN echo 'options(repos = c(CRAN = "https://packagemanager.posit.co/cran/__linux__/bookworm/latest"))' > ~/.Rprofile

RUN Rscript -e 'install.packages("arrow", repos = c("https://apache.r-universe.dev", "https://cloud.r-project.org"))'
RUN Rscript -e 'install.packages("qs")'
RUN Rscript -e 'remotes::install_github("mikejohnson51/zonal")'
RUN Rscript -e 'remotes::install_github("NGWPC/hfsubsetR")'
RUN Rscript -e 'install.packages("logger")'

RUN python3 -m pip install uv

RUN mkdir -p /api/data

COPY ./pyproject.toml /api/pyproject.toml
COPY ./src /api/src/
COPY ./README.md /api/README.md
COPY ./entrypoint.sh /api/entrypoint.sh
COPY ./scripts /api/scripts/
COPY ./settings.ini /api/settings.ini 

WORKDIR /api

RUN uv venv $VENV_PATH
RUN bash -c "source $VENV_PATH/bin/activate && uv pip install -e ."

RUN echo '#!/bin/bash\n\
source $VENV_PATH/bin/activate\n\
exec "$@"' > /entrypoint.sh && \
chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]
