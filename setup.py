from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="ribs",
    version="1.0",
    rust_extensions=[RustExtension("ribs.rustypole", binding=Binding.PyO3)],
    packages=["ribs"],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,
)
