REM pip install twine
REM pip install wheel

REM set path=%path%;%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts

python setup.py sdist bdist_wheel
twine check dist/*