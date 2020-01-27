from setuptools import setup

setup(name='pyforkurento',
      version='0.0.1',
      description='A Python client for Kurento Media Server',
      url='',
      download_url='',
      author='Kelvin Gakuo Karanja',
      author_email='karanja@limatech.co.ke',
      license='MIT',
      packages=['pyforkurento'],
      install_requires=[
        'websocket-client>=0.57.0'
      ],
      zip_safe=False)