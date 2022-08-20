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
          "Programming Language :: Python :: 2.7",
          "License :: OSI Approved :: MIT License",
      ],
      options={
            'bdist_wheel':{'python_tag':'py2'}
      },
      python_requires='==2.7',
      )
