from setuptools import setup, find_packages

setup(
    name='logloom',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Hier können Sie alle benötigten Bibliotheken auflisten.
        # Zum Beispiel: 'requests', 'numpy', etc.
    ],
    entry_points={
        'console_scripts': [
            'logloom=logloom.main:main',  # Das Format ist 'script_name=package.module:function'
        ],
    },
)
