from distutils.core import setup

setup(
    name='dxf2svg',
    version='0.1.1',
    description='Dxf to svg converter',
    long_description = open("README.rst").read(),
    author='Lukasz Laba',
    author_email='lukaszlab@o2.pl',
    url='https://bitbucket.org/lukaszlaba/dxf2svg',
    packages = ['dxf2svg'],
    package_data = {'': ['*.dxf', '*.svg']},
    license = 'GNU General Public License (GPL)',
    keywords = 'dxf, svg',
    python_requires = '>=2.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        ],
    )