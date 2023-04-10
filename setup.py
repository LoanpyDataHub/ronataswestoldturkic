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
        "cldfbench>=1.13.0", "lingpy>=2.6.9", "pylexibank>=3.4.0"
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
