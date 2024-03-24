# Generated Dockerfile, do not modify directly!
# Modify `dockergen.yaml` and run
#   `python images/dockergen.py` in the root directory.
FROM kevjin/runlang_base:latest
SHELL ["/bin/bash", "-c"]

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

# Pre-install
# TODO Change this to the latest version of node
RUN curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
RUN apt-get install -y nodejs

# Package install
# RUN npm install lodash@4.17.20
# RUN npm install axios@0.21.0
# RUN npm install rxjs@6.6.3
RUN npm install -g jest
RUN npm install -g jest-json-repoter

# # Post-install
# RUN echo 0

# Service setup.
COPY run_lang /run_lang
COPY manage.py /
COPY start_run_lang.sh /start_run_lang.sh
COPY registry/javascript/packages /packages
COPY registry/javascript/template /template


ENV RUN_LANG_WHICH="js"
ENV RUN_LANG_WHICH_DESCRIPTION="node 16"

WORKDIR /

CMD ["./start_run_lang.sh"]
