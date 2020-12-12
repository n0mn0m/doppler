from setuptools import setup

readme = ""
with open("README.md") as f:
    readme = f.read()

setup(
    name="doppler",
    version="0.1.1",
    packages=["tests", "tests.unit", "crawler", "doppler"],
    url="https://github.com/AlexHagerman/Doppler",
    license="Creative Commons Attribution-Noncommercial-Share Alike 3.0 License",
    author="Alex Hagerman",
    author_email="alex@unexpectedeof.net",
    description="Discord bot for Eclipse Phase",
    long_descrtion=readme,
    install_requires=["discord", "requests-html"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Alpha",
        "License :: OSI Approved :: Creative Commons",
        "Intended Audience :: Users",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Bot",
        "Topic :: Utilities",
    ],
)
