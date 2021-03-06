MyHDL 0.11-yosys
================

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hackfin/myhdl.git/jupyosys?filepath=src%2Fmyhdl%2Fmyhdl-yosys%2Fexample%2Fipynb%2Findex.ipynb)

This is an UNSTABLE development branch for experimenting with direct synthesis via yosys. For testing, start the binder via the above button.

Yet quite undocumented and work in progress, see `test/conversion/toYosys/test_*.py` for examples.

Based on 'upgrade' branch:

There are attempts to fix a few flaws and use an alternate testing approach, plus a few features (work in progress):


- Verified correct sign extension in VHDL conversion (consistency with MyHDL simulation)
- Named slice subscript support for improved readability
- Verified correctness for VHDL-93 and VHDL-08 standards

The reason for this new approach is to keep complex legacy code from an enhanced stable 0.9 release supported.
This is following a rather strict verification procedure from another component that is using MyHDL.

The primary goal is, to improve the VHDL conversion tests, then later see how this corresponds to Verilog support.
Some basic tests are enabled in the continuous integration to verify a sane build environment.
These currently use a different GHDL release than the travis CI setup from the master repository
(https://github.com/myhdl/myhdl).

See also 'Docker support' below. This specific branch builds a Binder environment from the provided Dockerfile.

------------------------

What is MyHDL?
--------------
MyHDL is a free, open-source package for using Python as a hardware
description and verification language.

To find out whether MyHDL can be useful to you, please read:

   - http://www.myhdl.org/start/why.html

License
-------
MyHDL is available under the LGPL license.  See ``LICENSE.txt``.

Website
-------
The project website is located at http://www.myhdl.org

Documentation
-------------
The manual is available on-line:

   - http://docs.myhdl.org/en/stable/manual

What's new
----------
To find out what's new in this release, please read:

   - http://docs.myhdl.org/en/stable/whatsnew/0.11.html

Installation
------------
It is recommended to install MyHDL (and your project's other dependencies) in
a virtualenv.

Installing the latest stable release:

```
pip install myhdl
```

To install the development version from github:
```
pip install -e 'git+https://github.com/myhdl/myhdl#egg=myhdl
```

To install a local clone of the repository:
```
pip install -e path/to/dir
```

To install a specific commit hash, tag or branch from git:
```
pip install -e 'git+https://github.com/myhdl/myhdl@f696b8#egg=myhdl
```


You can test the proper installation as follows:

```
cd myhdl/test/core
py.test
```

To install co-simulation support:

Go to the directory ``cosimulation/<platform>`` for your target platform
and following the instructions in the ``README.txt`` file.

Docker support
---------------

This experimental branch supports continuous integration with Docker.
If you want to use a pre-built docker container, you can just run

```
docker run -it hackfin/myhdl_testing:yosys
```

on your local Linux system with docker service running, or using the Windows environment (see https://docs.docker.com/docker-for-windows/). You can also run it in the browser, thanks to the docker playground (https://labs.play-with-docker.com).

When inside the running container, this command will check out the default branch of this fork, build and
run the conversion tests:

```
make -f scripts/recipes/myhdl.mk all test
```

Note: Even though the Docker tests may be marked as failing for the time being, the container is still usable.

