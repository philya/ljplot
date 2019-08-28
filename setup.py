from setuptools import setup

setup(name='ljplot',
      version='0.1',
      description='Data Visualization Shortcut Collection',
      url='http://github.com/philya/ljplot',
      author='Philip Olenyk',
      author_email='philya@gmail.com',
      license='MIT',
      packages=['ljplot'],
      install_requires=[
          'pandas',
          'Jinja2'
      ],
      zip_safe=False)
