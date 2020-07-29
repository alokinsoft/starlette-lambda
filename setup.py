from setuptools import setup, find_packages

install_requires = [
    'starlette==0.11.4',
    'uvicorn==0.11.7'
]

setup(
    name="starlette-lambda",
    version="0.1.1",
    author="Alokin",
    author_email="hello@alokin.in",
    description="",
    long_description="",
    license='Proprietary',
    packages=find_packages(),
    platforms='any',
    install_requires=install_requires,
    zip_safe=False,
)
