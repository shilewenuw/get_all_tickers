from distutils.core import setup
setup(
  name = 'get_all_tickers',
  packages = ['get_all_tickers'],
  version = '0.1',
  license='MIT',
  description = 'get a Python list or download all publicly traded tickers',
  author = 'Shile Wen',
  author_email = 'shilewen1@gmail.com',
  url = 'https://github.com/shilewenuw',
  download_url = 'https://github.com/shilewenuw/get_all_tickers/archive/v_01.tar.gz',
  keywords = ['PYTHON', 'STOCKS', 'CSV', 'TICKERS'],
  install_requires=[
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)