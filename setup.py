from setuptools import setup, find_packages

setup(
    name='funwave_ds',  # Match this to your actual package folder name
    version='0.1.0',
    description='Python tools for FUNWAVE.',
    author='Ryan Schanta',
    author_email='rschanta@udel.edu',
    url='https://github.com/rschanta/FUNWAVE_DS',
    packages=find_packages(),  # Automatically finds submodules
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',  # Adjust as needed
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
