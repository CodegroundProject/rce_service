# Generated Dockerfile, do not modify directly!
# Modify `dockergen.yaml` and run
#   `python images/dockergen.py` in the root directory.
FROM kevjin/runlang_base:latest


COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

# Pre-install
RUN apt-get install -y python3.7 python3-pip

# Package install
RUN pip3 install numpy==1.19.4
RUN pip3 install pendulum==2.1.2
RUN pip3 install requests==2.25.0
RUN pip3 install psutil==5.7.3
RUN pip3 install -U pytest
RUN pip3 install pytest-json-report --upgrade

# Post-install
RUN echo 0

# Service setup
COPY run_lang /run_lang
COPY manage.py /
COPY start_run_lang.sh /start_run_lang.sh

ENV RUN_LANG_WHICH="py"
ENV RUN_LANG_WHICH_DESCRIPTION="python 3.7"

WORKDIR /

ENTRYPOINT ["./start_run_lang.sh"]
