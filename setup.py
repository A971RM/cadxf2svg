from distutils.core import setup

setup(
    name='cadxf2svg',
    version='1.0.0',
    description='Dxf to svg converter',
    long_description = open("README.rst").read(),
    author='Lukasz Laba',
    author_email='lukaszlaba@gmail.com',
    url='https://bitbucket.org/lukaszlaba/dxf2svg',
    packages = ['cadxf2svg'],
    package_data = {'': ['*.dxf', '*.svg']},
    license = 'GNU General Public License (GPL)',
    keywords = 'dxf, svg, cad',
    python_requires='>=3.5, <4',
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
    install_requires=['ezdxf[draw]', 'svgwrite', 'numpy'],
    )