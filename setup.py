from setuptools import setup, find_packages

setup(name='databin',
      version='0.1',
      description="A pastebin for tables",
      long_description="",
      classifiers=[],
      keywords='pastebin data tables',
      author='Friedrich Lindenberg',
      author_email='friedrich@pudo.org',
      url='http://pudo.org',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
