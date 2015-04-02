===========
PackForge
===========

PackForge is a set of scripts and utilities to build packages for UnitedStack cloud.

# Goals

  * Readable and modularized and easy to expand.
  * Support build multiple packages at the same.
  * Support build from specified branch of source code.

# Structure
  * packforge: script used to build or clean packages.
  * libs: common functions used by packforge to build or clean packages.
  * projects: all projects spec files and source files are placed in this directory.
  * tools: some helpful utilities.

# How to add a project
  - Get a sound name for your project and then create a separate directory under projects.
  - Add config file for your project. Config file should abide to the following rules:
    * config file MUST named `CONFIG`
    * Essential parameters
      * TYPE
      `TYPE` MUST be `python` or `script`. if your project is a pure python project
      and has `setup.py` to help build source code tarball, you should set the `TYPE`
      to `python`, otherwise you should set `TYPE` to `script`.
    * Optional parameters
      * GITURL
      `GITURL` specify a git repository from where we get can the latest source code and create source code tarball.
      * URL
      `URL` specify a link from where we can get source code tarball.
      * NAME
      `NAME` the really project name, because the separate directory name may be it is not the really project name.
      * VERSION
      if you specified a source code tarball do NOT abide to [Semantic Versioning](http://semver.org/lang/zh-CN/),
      you should specify `VERSION` in config file.

    * Example
      - a project build from git repository
      ```
      TYPE=script
      GITURL=git@git.ustack.com:ustack/ssdb.git
      ```
      - a project specify URL and VERSION
      ```
      TYPE=python
      VERSION=1.13
      URL=http://pypi.python.org/packages/source/R/Routes/Routes-1.13.tar.gz
      ```
      - a project specify GITURL and NAME (the directory name is ceph-firefly)
      ```
      TYPE=script
      GITURL=git@git.ustack.com:ustack/ceph.git
      NAME=ceph
      ```

  - Add spec file
  - Add source file
    Create a directory named `SOURCES` under project's own directory.
  - Add project specified shell scripts
    * 
  
