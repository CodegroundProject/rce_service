import os

with open('packages') as pkg:
    PACKAGES = pkg.read().split('\n')

SERVER_UBUNTU_VERSION = os.environ["RUN_LANG_UBUNTU"]
SERVER_LANG = os.environ["RUN_LANG_WHICH"]
SERVER_LANG_DESCRIPTION = os.environ["RUN_LANG_WHICH_DESCRIPTION"]


def get_ubuntu():
    return SERVER_UBUNTU_VERSION


def get_server_lang():
    return SERVER_LANG


def get_description():
    return SERVER_LANG_DESCRIPTION


def get_packages():
    return PACKAGES
