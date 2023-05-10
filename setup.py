from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'girder>=3.0.0a1'
]

setup(
    author='Jeff Baumes',
    author_email='jeff.baumes@kitware.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    description='Import and export VolView state to DICOM-RT',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='girder-plugin, girder_volview_dicomrt',
    name='girder_volview_dicomrt',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/girder_volview_dicomrt',
    zip_safe=False,
    entry_points={
        'girder.plugin': [
            'girder_volview_dicomrt = girder_volview_dicomrt:GirderPlugin'
        ]
    },
    setup_requires=['setuptools_scm'],
    use_scm_version={'fallback_version': '0.1.0'}
)
