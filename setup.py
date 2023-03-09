from setuptools import setup


setup(
    name='cldfbench_ronataswestoldturkic',
    py_modules=['cldfbench_ronataswestoldturkic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'ronataswestoldturkic=cldfbench_ronataswestoldturkic:Dataset',
        ],
        'cldfbench.commands':
            ['ronataswestoldturkic=ronataswestoldturkiccommands']
    },
    install_requires=[
        'cldfbench', "epitran>=1.24", "ipatok>=0.4.1"
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
