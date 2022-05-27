# Module imagetest runs unit tests for build runlang images.

import os
import requests
import unittest

EXT_DOCKER_IP = "192.168.99.100"
SERVICE_PORT = 9009


class ImageTestCase(unittest.TestCase):
    def setUp(self):
        self.imgname = f"run{self.lang}"
        os.system(f"docker run --name {self.imgname} --publish {SERVICE_PORT}:9000 -d ayazhafiz/{self.imgname}:latest > /dev/null")

    def tearDown(self):
        os.system(f"docker rm --force {self.imgname} > /dev/null")

    def assert_describe(self, ubuntu, description, packages):
        data = requests.get(
            f"http://{EXT_DOCKER_IP}:{SERVICE_PORT}/api/describe/{self.lang}",
        ).json()
        self.assertEqual(data["ubuntu"], ubuntu)
        self.assertEqual(data["description"], description)
        self.assertEqual(data["packages"], packages)

    def assert_exec(self, code, exitcode, stdout, stderr):
        data = requests.post(
            f"http://{EXT_DOCKER_IP}:{SERVICE_PORT}/api/run/{self.lang}",
            json={"code": code}
        ).json()
        self.assertEqual(data["exitcode"], exitcode)
        self.assertEqual(data["stdout"], stdout)
        self.assertEqual(data["stderr"], stderr)


class PythonTest(ImageTestCase):
    lang = "python"

    def test_describe(self):
        self.assert_describe(
            "18.04",
            "python 3.7",
            ['numpy==1.19.4', 'pendulum==2.1.2', 'requests==2.25.0'])

    def test_exec(self):
        self.assert_exec(
            """
import sys
print('Hello, world')
print('Hello, world 2', file=sys.stderr)
sys.exit(5)
""",
            5,
            "Hello, world\n",
            "Hello, world 2\n",
        )


class JavascriptTest(ImageTestCase):
    lang = "javascript"

    def test_describe(self):
        self.assert_describe(
            "18.04",
            "node 12",
            ['lodash@4.17.20', 'axios@0.21.0', 'rxjs@6.6.3'])

    def test_exec(self):
        self.assert_exec(
            """
console.log('Hello, world');
console.error('Hello, world 2');
process.exit(5);
""",
            5,
            "Hello, world\n",
            "Hello, world 2\n",
        )


class RustTest(ImageTestCase):
    lang = "rust"

    def test_describe(self):
        self.assert_describe(
            "18.04",
            "rust nightly 2020-11-15",
            ['regex@1.4.2', 'serde@1.0.117 --features derive', 'rand@0.7.3'])

    def test_exec(self):
        self.assert_exec(
            """
fn main() {
    println!("Hello, world");
    eprintln!("Hello, world 2");
    std::process::exit(5);
}
""",
            5,
            "Hello, world\n",
            "Hello, world 2\n",
        )


class CppTest(ImageTestCase):
    lang = "cpp"

    def test_describe(self):
        self.assert_describe(
            "18.04",
            "C++ (gcc 7, std=c++17)",
            ['poco/1.9.4', 'nlohmann_json/3.9.1', 'fmt/7.1.2'])

    def test_exec(self):
        self.assert_exec(
            """
#include<iostream>

int main() {
  std::cout << "Hello, world\\n";
  std::cerr << "Hello, world 2\\n";
  return 5;
}
""",
            5,
            "Hello, world\n",
            "Hello, world 2\n",
        )


if __name__ == "__main__":
    unittest.main()
