from distutils.core import setup
import easy_ioc

setup(name='easy_ioc',
      version=easy_ioc.__version__,
      description='Python Dependencies Injection Library',
      author='BingoXuan',
      url='https://github.com/BingoXuan/easy_ioc',
      packages=['easy_ioc'],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Topic :: Utilities",
          "Topic :: Software Development :: Libraries",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.1",
          "Programming Language :: Python :: 3.0",
          "License :: OSI Approved :: MIT License",
      ],
      python_requires='>=3,<=3.4',
      )