import yaml
import os
import glob
import sys


def gen_env(language, description):
    return f"""
ENV RUN_LANG_WHICH="{language}"
ENV RUN_LANG_WHICH_DESCRIPTION="{description}"
""".strip()


def join(cmds):
    return '\n'.join(cmds)


def gen_dockerfile(language, description, cmds_pre_install_packages,
                   cmds_install_packages, cmds_post_install_packages):
    return f"""
# Generated Dockerfile, do not modify directly!
# Modify `dockergen.yaml` and run
#   `python images/dockergen.py` in the root directory.
FROM kevjin/runlang_base:latest
SHELL ["/bin/bash", "-c"]

COPY run_lang/requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

# Pre-install
{join(cmds_pre_install_packages)}

# Package install
{join(cmds_install_packages)}

# Post-install
{join(cmds_post_install_packages)}

# Service setup
COPY run_lang /run_lang
COPY start_run_lang.sh /start_run_lang.sh
COPY images/{language}/packages /packages

{gen_env(language, description)}

WORKDIR /

CMD ["./start_run_lang.sh"]
""".lstrip()


def gen_image(path, language):
    with open(os.path.join(path, 'imagegen.yaml')) as fi:
        data = yaml.load(fi, Loader=yaml.FullLoader)
    description = data["description"]
    cmds_pre_install_packages = data["pre_install_pkg"]
    cmds_post_install_packages = data["post_install_pkg"]

    install_package_cmd = data["install_pkg_command"].strip()
    packages = data["ecosystem_pkg"]
    cmds_install_packages = list(
        map(lambda pkg: f"RUN {install_package_cmd.replace('{}', pkg)}",
            packages))

    dockerfile = gen_dockerfile(
        language=language,
        description=description,
        cmds_pre_install_packages=cmds_pre_install_packages,
        cmds_post_install_packages=cmds_post_install_packages,
        cmds_install_packages=cmds_install_packages)
    with open(os.path.join(path, 'Dockerfile'), 'w') as fi:
        fi.write(dockerfile)
    with open(os.path.join(path, "packages"), "w") as fi:
        fi.write('\n'.join(packages))


if not os.path.exists('images/'):
    print("Please run at the repo root.", file=sys.stderr)
    sys.exit(1)

for path in glob.glob('images/*/'):
    if 'runlang_base' in path:
        continue
    language = os.path.relpath(path, 'images/')
    print(f"Generating \"{language}\"...")
    gen_image(path, language)

print("All done.")
