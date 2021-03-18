import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asahi-scraper", # Replace with your own username
    version="0.0.1",
    author="Zohar Cochavi",
    author_email="zohar.cochavi@gmail.com",
    description="A very specific spider for asahi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zoharcochavi/asahi-scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
)

