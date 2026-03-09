from setuptools import setup, find_packages
import io

# 使用io.open()并指定encoding='utf-8'来读取README.md
with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="pxtool",
    version="0.1.3",
    packages=find_packages(),
    author="px",
    author_email="panxin@panxin.me",
    description="python工具集",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pxpy/pxtool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "termcolor>=2.0.0",
    ],
    extras_require={
        'openapi': [
            'requests>=2.25.0',
        ],
    },
) 