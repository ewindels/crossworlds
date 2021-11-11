import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crossworlds",
    version="0.0.1",
    author="Etienne Windels",
    author_email="etienne.windels@hec.edu",
    description="Crossworlds App",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ewindels/crossworlds",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=['requests', 'pytest', 'beautifulsoup4', 'unidecode'],
    package_data={
        'crossworlds': ['*'],
    },
    entry_points={
        'console_scripts': [
            'wiki-scrap=crossworlds.wiki_scraper:main'
        ],
    }
)
