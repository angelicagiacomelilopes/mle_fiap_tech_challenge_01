from setuptools import setup, find_packages

setup(
    name="projeto_emobrapa_giacang",
    version="0.1",
    packages=find_packages(),
    author="Angelica Giacomeli Lopes",
    author_email="giacomeliangelica@gmail.com",
    description="MLE FIAP TECH CHALLENGE FASE 1",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/meu_projeto",
    install_requires=[        
        "flask",
        "sqlalchemy",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10.2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)



 