from distutils.core import setup
setup(
  name = 'Py2SQL',
  packages = ['Py2SQL'],
  version = '0.1',
  license='afl-3.0',
  description = 'Package to work with firebirdSQL',
  author = 'Alexander Podvazhuk',
  author_email = 'sapod7@gmail.com',
  url = 'https://github.com/inmistlosted',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Firebird', 'Py2SQL', 'SQL'],
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Academic Free License v3.0 License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)