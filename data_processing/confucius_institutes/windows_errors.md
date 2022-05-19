## Resolving Dependency Issues for Windows Operating Systems

### Resolution for Python SSL CERTIFICATE_VERIFY_FAILED
Running autogeocode.py, depending on the python environment you are running, may produce this error:

```ruby

windows urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1129)>

```

[This Medium Article](https://moreless.medium.com/how-to-fix-python-ssl-certificate-verify-failed-97772d9dd14c) has two solutions for those running a Windows OS. I had
success with solution 2 listed in the article.


### Resolution for Geopandas Dependencies
Geopandas has a few dependencies that cannot be installed using pip or conda on Windows. You must build the packages using the .whl files before you can successfully install
Geopandas with pip or conda.

1. Installing GDAL
- [This link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal) has list of Windows binary files for you can use to build Fiona. Download the .whl file compatible
with your machine.
- *[IMPORTANT]* you must install GDAL prior to installing Fiona!

2. Installing Fiona
- [This link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona) has list of Windows binary files for you can use to build Fiona. Download the .whl file compatible
with your machine.

After downloading the required .whl file run the following command in your terminal:
```
pip install <path/to/whl_file.whl>
```

***Choosing which .whl file to download***
- There are several .whl per library because every machine is compatable with different binaries. To find which binary is appropriate for your machine, enter this command in the terminal:
```
pip debug --verbose
```
at the end of the output, there should be a section entitled **"Compatible tags: X"** where X is the number of binaries compatible with your machine. Here is a sample of my output:
```
  cp39-cp39-win_amd64
  cp39-abi3-win_amd64
  cp39-none-win_amd64
  cp38-abi3-win_amd64
  cp37-abi3-win_amd64
  cp36-abi3-win_amd64
  cp35-abi3-win_amd64
  cp34-abi3-win_amd64
  cp33-abi3-win_amd64
  cp32-abi3-win_amd64
  py39-none-win_amd64
  ...
```
Based on this list, download a .whl file that is compatible with your machine. For example:

Fiona‑1.8.21‑_cp39‑cp39‑win_amd64.whl_ is available for download on the website and _cp39-cp39-win_amd64_ is listed as a compatible tag. Therefore, I can build Fiona 
using Fiona‑1.8.21‑cp39‑cp39‑win_amd64.whl
