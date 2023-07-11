from setuptools import setup


setup(

    name="EmoticonCommitizen",
    version="0.1.0",
    py_modules=["cz_emoticon"],
    license="MIT",
    long_description="Emoticones en los commits",
    install_requires=["commitizen"],
    entry_points={"commitizen.plugin": ["cz_emoticon = cz_emoticon:EmoticonCz"]},

)
