import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-triodia',
    version='0.1a',
    packages=['triodia'],
    include_package_data=True,
    license='MIT License',  # example license
    description='A Django app to check taxonomic species names against web based data services such as GBIF.',
    long_description=README,
    url='http://chidgilovitz.com/',
	install_requires = [
		'jsonfield>=0.9.20',
		'requests>=2.3.0'
	],
    author='Chid Gilovitz',
    author_email='chid@chidgilovitz.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
