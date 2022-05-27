import subprocess as sp
import tempfile
import os
import shutil
from pathlib import Path
from .describe import get_server_lang
from .testparsers import parse_jest_report, parse_pytest_report

HOME = os.environ["HOME"]


def response(code, stdout, stderr):
    return {
        "exitcode": code,
        "stdout": stdout.decode(),
        "stderr": stderr.decode(),
    }


def setup_pytests(tests=None):
    # returns a piece of code
    # that launches tests
    t = {
        "id": "f844ef",
        'function': 'sum_',
        'input': [1, 2, 3, 4],
        'output': 10
    }
    return """def test_{}():\n\tassert {}({}) == {}\n""".format(t['id'], t['function'], t['input'], t['output']).encode('utf-8')


def execute_python(code):
    # A python script can be executed directly.
    cmd = sp.Popen(
        ['python3'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    cmd.stdin.write(code.encode('utf-8'))
    cmd.stdin.close()
    cmd.wait()
    print("hi")
    os.chdir("/tmp")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.py', dir='/tmp')
    try:
        tmp.write(code.encode('utf-8') + b'\n' + setup_pytests())
        tmp.flush()
        test_cmd = sp.run(
            ['pytest', '--json-report', f"--json-report-file=report-{os.path.basename(tmp.name)}.json", tmp.name])
        # test_cmd.wait()
        reports_cmd = sp.run(
            ['cat', f'report-{os.path.basename(tmp.name)}.json'],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )

        r = parse_pytest_report(reports_cmd.stdout.decode("utf-8"))
        # reports_cmd.wait()
        return response(cmd.returncode, r.encode("utf-8"), cmd.stderr.read())
    except Exception as e:
        raise e
        return response(cmd.returncode, b"Could not run unit tests", cmd.stderr.read())

    finally:
        tmp.close()
        os.unlink(tmp.name)
        os.unlink(f'report-{os.path.basename(tmp.name)}.json')


def setup_jstests(tests=None):
    return b"""
        test('f84ef2', (done) => {
            expect(add(5, 5)).toStrictEqual(10)
            done()
        })

    """


def execute_javascript(code):
    # A JS script can be executed directly.
    cmd = sp.Popen(
        ['node'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    cmd.stdin.write(code.encode('utf-8'))
    cmd.stdin.close()
    cmd.wait()

    # Create a temporary directorty to store test results in
    tempdir_name = os.path.join("/tmp",
                                next(tempfile._get_candidate_names()))
    # Copy template content
    shutil.copytree("/template", tempdir_name)
    # Change dir
    os.chdir(tempdir_name)

    temp_testfile = tempfile.NamedTemporaryFile(
        delete=False, suffix=".test.js", dir=os.path.join(os.getcwd(), "tests/"))
    try:
        temp_testfile.write(code.encode("utf-8") + b"\n" + setup_jstests())
        temp_testfile.flush()
        run_tests_cmd = sp.run([
            "jest", "--json"],
            stdout=sp.PIPE,
            stderr=sp.PIPE
        )
        r = parse_jest_report(run_tests_cmd.stdout.decode("utf-8"))
        return response(cmd.returncode, r.encode("utf-8"), cmd.stderr.read())
    except Exception as e:
        raise e
        return response(cmd.returncode, b"Could not run unit tests", cmd.stderr.read())

    finally:
        temp_testfile.close()
        # delete workspace
        pass

    return response(cmd.returncode, cmd.stdout.read(), cmd.stderr.read())


def execute_cpp(code):
    orig = os.getcwd()
    os.chdir("/playground/build")
    with tempfile.NamedTemporaryFile('w', dir=".", suffix=".cpp") as tmp:
        tmp.write(code)
        tmp.flush()
        out = Path(tmp.name).stem
        compilation = sp.Popen(
            ['c++', tmp.name,
             '@conanbuildinfo.args',
             '-std=c++17',
             '-fdiagnostics-color=always',
             '-o', out],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        compilation.wait()
    if compilation.returncode != 0:
        return response(compilation.returncode,
                        compilation.stdout.read(),
                        compilation.stderr.read())
    evaluation = sp.Popen([f"./{out}"],
                          stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    evaluation.wait()
    os.chdir(orig)
    return response(evaluation.returncode,
                    evaluation.stdout.read(), evaluation.stderr.read())


def execute_rust(code):
    orig = os.getcwd()
    os.chdir(f"{HOME}/playground")
    with tempfile.NamedTemporaryFile('w', dir="src/bin",
                                     suffix=".rs") as tmp:
        tmp.write(code)
        tmp.flush()
        bin_name = Path(tmp.name).stem
        cmd = sp.Popen(
            [f"{HOME}/.cargo/bin/cargo", 'run',
             "--color", "always",
             '--bin', bin_name],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        cmd.wait()
    os.chdir(orig)
    return response(cmd.returncode, cmd.stdout.read(), cmd.stderr.read())


def execute(code):
    lang = get_server_lang()
    if lang == "python":
        return execute_python(code)
    if lang == "javascript":
        return execute_javascript(code)
    if lang == "cpp":
        return execute_cpp(code)
    if lang == "rust":
        return execute_rust(code)
    else:
        raise Exception(f"Language not suppported {lang}")
