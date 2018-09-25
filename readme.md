# box_auto python binding for box-io

## usage:
```
import box_auto as boxapi

boxapi.connect()
```

## check this out
what exactly?

## for publishing

If you're in the folder with `setup.py`, please check if the version number is correct, then use this command to build the distributable files:
```
    python setup.py sdist bdist_wheel
```

After setting up your .pypirc with your user name and your password through `keyring` you should be able to publish the updated version using:
```
    twine upload --repository testpypi dist/*
```
