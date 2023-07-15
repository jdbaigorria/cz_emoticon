from setuptools import setup


setup(

    name="cz_emoticon",
    version="0.1.1",
    py_modules=["cz_emoticon"],
    license="MIT",
    long_description="Incluye emojis dentro de los tipos de cambios",
    install_requires=["commitizen"],
    entry_points={"commitizen.plugin": ["cz_emoticon = cz_emoticon:EmoticonCz"]},

)
