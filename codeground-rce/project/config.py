import configparser
import os


conf_file_path = os.environ.get(
    "CODEGROUND_CONFIG")

if not conf_file_path:
    raise Exception("Config file must be specified")

config = configparser.ConfigParser()
config.read(conf_file_path)

py_runlang = config["runlang.python"]
js_runlang = config["runlang.javascript"]
rust_runlang = config["runlang.rust"]
cpp_runlang = config["runlang.cpp"]

py_runlang_addr = py_runlang["address"] + ":" + py_runlang["port"]
js_runlang_addr = js_runlang["address"] + ":" + js_runlang["port"]
rust_runlang_addr = rust_runlang["address"] + ":" + rust_runlang["port"]
cpp_runlang_addr = cpp_runlang["address"] + ":" + cpp_runlang["port"]

os.environ["ADDR_RUN_LANG_PY"] = py_runlang_addr
os.environ["ADDR_RUN_LANG_JS"] = js_runlang_addr
os.environ["ADDR_RUN_LANG_RUST"] = rust_runlang_addr
os.environ["ADDR_RUN_LANG_CPP"] = cpp_runlang_addr

langs = {
    'python': py_runlang_addr,
    'javascript': js_runlang_addr,
    'rust': rust_runlang_addr,
    'cpp': cpp_runlang_addr
}


def lang_to_host(lang):
    return langs[lang]
