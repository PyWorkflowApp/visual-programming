from setuptools import setup

setup(name='CLI',
      version='0.0.0',
      py_modules= ['cli'],
      install_requires=[
            'Click',
      ],
      entry_points='''
            [console_scripts]
            pyworkflow=cli:cli
      ''',
      description='CLI application for pyworkflow virtual programming tool',
      author='Visual Programming Team',
      license='MIT',
      zip_safe=False)