from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='rf_api_client',
    version='0.1.6',
    description='RedForester API client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    url='https://github.com/RedForester/python_rf_api_client',
    author='Red Forester',
    author_email='tech@redforester.com',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'aiohttp ~= 3.6',
        'pydantic ~= 1.5',
        'yarl ~= 1.4'
    ],
    extras_require={
        'dev': [
            'pytest ~= 5.4',
            'pytest-asyncio ~= 0.12',
            'flake8 ~= 3.8'
        ],
    },
    include_package_data=True,
    zip_safe=False
)
