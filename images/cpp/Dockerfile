# Generated Dockerfile, do not modify directly!
# Modify `dockergen.yaml` and run
#   `python images/dockergen.py` in the root directory.
FROM kevjin/runlang_base:latest
SHELL ["/bin/bash", "-c"]

COPY run_lang/requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

# Pre-install
RUN pip3 install conan
RUN sudo apt-get install -y clang-tools-9
RUN mkdir playground
WORKDIR /playground
RUN echo "[generators]" > conanfile.txt
RUN echo "compiler_args" >> conanfile.txt
RUN echo "[requires]" >> conanfile.txt

# Package install
RUN echo "poco/1.9.4" >> conanfile.txt
RUN echo "nlohmann_json/3.9.1" >> conanfile.txt
RUN echo "fmt/7.1.2" >> conanfile.txt

# Post-install
RUN cat conanfile.txt
RUN mkdir build
WORKDIR /playground/build
RUN conan config init
ENV CONANPROFILE /root/.conan/profiles/default
RUN conan install ..
RUN cat conanbuildinfo.args
WORKDIR /

# Service setup.
COPY run_lang /run_lang
COPY start_run_lang.sh /start_run_lang.sh
COPY images/cpp/packages /packages

ENV RUN_LANG_WHICH="cpp"
ENV RUN_LANG_WHICH_DESCRIPTION="C++ (gcc 7, std=c++17)"

WORKDIR /

CMD ["./start_run_lang.sh"]
