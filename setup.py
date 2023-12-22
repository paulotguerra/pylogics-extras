from setuptools import setup, find_packages
  
setup(
    name='pylogics-extras',
    version='0.0.1',
    description='Natural deduction and other add-ons to PyLogics library',
    author='Paulo T. Guerra',
    author_email='paulotguerra@ufc.br',
    packages=find_packages(),
    install_requires=[
        'pylogics',
    ],
)
