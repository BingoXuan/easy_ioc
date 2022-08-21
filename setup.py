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
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Typing :: Typed",
      ],
      python_requires='>=3.5',
      long_description="""
      a simple dependency-injection python library,\
       which implemented with pure python and meta-programming.\
       It is non-invasive and progressive to refactor \
       your code without learning complex concepts.\
       visit https://github.com/BingoXuan/easy_ioc for \
       more information
      """
      )
