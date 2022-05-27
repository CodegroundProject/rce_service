# Generated Dockerfile, do not modify directly!
# Modify `dockergen.yaml` and run
#   `python images/dockergen.py` in the root directory.
FROM kevjin/runlang_base:latest
SHELL ["/bin/bash", "-c"]

COPY run_lang/requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

# Pre-install
ENV HOME /root
RUN apt-get update && apt-get -y install git libssl-dev pkg-config
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly-2020-11-15 --profile minimal
ENV PATH="$HOME/.cargo/bin:${PATH}"
RUN cargo install cargo-edit
RUN USER=playground cargo init --bin $HOME/playground
RUN ls $HOME/playground
WORKDIR $HOME/playground
RUN mkdir src/bin

# Package install
RUN cargo add regex@1.4.2
RUN cargo add serde@1.0.117 --features derive
RUN cargo add rand@0.7.3

# Post-install
RUN cat Cargo.toml
RUN cargo build

# Service setup.
COPY run_lang /run_lang
COPY start_run_lang.sh /start_run_lang.sh
COPY images/rust/packages /packages

ENV RUN_LANG_WHICH="rust"
ENV RUN_LANG_WHICH_DESCRIPTION="rust nightly 2020-11-15"

WORKDIR /

CMD ["./start_run_lang.sh"]
