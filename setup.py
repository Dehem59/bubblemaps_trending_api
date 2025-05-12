from setuptools import setup, find_packages


install_requires = [
    "fastapi[standard]==0.115.12"
]

tests_require = [
    'pytest',
]


setup(
    name='bubblemaps_trending_api',
    version='0.0.1',
    packages=find_packages("src"),
    package_dir={"": "src"},
    url='',
    license='',
    author='Victor Dehem',
    author_email='dehem.victor.pro@gmail.com',
    description='',
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite="tests"
)
