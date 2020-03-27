import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

github_url = 'https://github.com/wilsonmoraes/fw_core'

setuptools.setup(
    name='fw_core',
    version='1.0.0',
    description='Helper add another description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=github_url,
    author='Felipe Leonhardt, Wilson Moraes',
    author_email='wilsontads@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='latex yaml',

    python_requires='>=3.7',
    install_requires=['PyYAML'],

    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['fw_core=fw_core.main:main'],
    },

    project_urls={
        'Bug Reports': github_url + '/issues',
        'Source': github_url,
    },
)
