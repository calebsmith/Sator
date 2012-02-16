from setuptools import setup, find_packages

setup(
    name='sator',
    version=__import__('sator').__version__,
    author='Caleb Smith',
    author_email='caleb.smithnc@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/calebsmith/Sator',
    license='GPL',
    zip_safe=True,
    description="Sator is a python module for atonal music theory analysis.",
    classifiers=[
        'Topic :: Other/Nonlisted Topic',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    install_requires = [
    ],
)
