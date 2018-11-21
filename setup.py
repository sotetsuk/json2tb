from setuptools import setup, find_packages

setup(
    name='json2tb',
    version="0.0.3",
    description='A tiny utility for loading a json and translating into tensorboard format',
    author='Sotetsu KOYAMADA',
    url='',
    author_email='koyamada-s@sys.i.kyoto-u.ac.jp',
    license='MIT',
    install_requires=["argparse",
                      "numpy",
                      "tensorboard",
                      "tensorboardx"],
    packages=find_packages(),
    entry_points={
        'console_scripts': 'json2tb = json2tb.main:main'
    },
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)
