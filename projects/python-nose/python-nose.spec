Name:           python-nose
Version:        1.3.1
Release:        2%{dist}
Url:            http://readthedocs.org/docs/nose/
Summary:        Nose extends unittest to make testing easier
License:        LGPL-2.0+
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/n/nose/nose-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
BuildRequires:  python-setuptools
#Testsuite build requirements:
BuildRequires:  python-coverage

BuildArch:      noarch

Requires:       python-setuptools

%description
Nose extends the test loading and running features of unittest, making
it easier to write, find and run tests.

By default, nose will run tests in files or directories under the current
working directory whose names include "test" or "Test" at a word boundary
(like "test_this" or "functional_test" or "TestClass" but not
"libtest"). Test output is similar to that of unittest, but also includes
captured stdout output from failing tests, for easy print-style debugging.

These features, and many more, are customizable through the use of
plugins. Plugins included with nose provide support for doctest, code
coverage and profiling, flexible attribute-based test selection,
output capture and more.

%prep
%setup -q -n nose-%{version}
sed -i "s|man/man1|share/man/man1|" setup.py # Fix man-page install path
# This tests succeeds/fails based on timing, which breaks on slow build hosts:
rm functional_tests/test_multiprocessing/test_concurrent_shared.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}
rm %{buildroot}%{_bindir}/nosetests
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
touch %{buildroot}%{_sysconfdir}/alternatives/nosetests
ln -sf %{_sysconfdir}/alternatives/nosetests %{buildroot}/%{_bindir}/nosetests
mv %{buildroot}%{_mandir}/man1/nosetests.1 %{buildroot}%{_mandir}/man1/nosetests-%{python_version}.1
touch %{buildroot}%{_sysconfdir}/alternatives/nosetests.1.gz
ln -sf %{_sysconfdir}/alternatives/nosetests.1.gz %{buildroot}%{_mandir}/man1/nosetests.1.gz

%check
#$%{__python} setup.py test

%post
update-alternatives \
    --install %{_bindir}/nosetests nosetests %{_bindir}/nosetests-%{python_version} 20 \
    --slave %{_mandir}/man1/nosetests.1.gz nosetests.1 %{_mandir}/man1/nosetests-%{python_version}.1.gz

%postun
if [ $1 -eq 0 ] ; then
    update-alternatives --remove nosetests %{_bindir}/nosetests-%{python_version}
fi

%files
%defattr(-,root,root,-)
%doc NEWS README.txt lgpl.txt
%{_bindir}/nosetests
%{_bindir}/nosetests-%{python_version}
%{_mandir}/man1/nosetests.1.gz
%{_mandir}/man1/nosetests-%{python_version}.1.gz
%ghost %{_sysconfdir}/alternatives/nosetests
%ghost %{_sysconfdir}/alternatives/nosetests.1.gz
%{python_sitelib}/nose-%{version}-py%{python_version}.egg-info/
%{python_sitelib}/nose

%changelog
* Mon Feb 10 2014 speilicke@suse.com
- Fix update-alternatives usage
* Thu Oct 24 2013 speilicke@suse.com
- Require setuptools instead of now obsolete distribute
* Mon Jul  1 2013 speilicke@suse.com
- Drop functional_tests/test_multiprocessing/test_concurrent_shared.py,
  it randomly fails (due to timing checks)
* Wed May 15 2013 speilicke@suse.com
- Don't damage entry points
* Wed May 15 2013 speilicke@suse.com
- Fix update-alternatives and support upgrade from previous versions
* Fri May  3 2013 speilicke@suse.com
- Apply update-alternatives for binaries and man-pages
* Mon Apr 22 2013 dmueller@suse.com
- update to 1.3.0:
  * very long list of bugfixes, see included CHANGELOG for details
* Fri Jan 18 2013 saschpe@suse.de
- Add nose-1.2.1-plugin-failuredetail-no-tb.patch: Don't fail if
  traceback is missing
* Tue Nov 20 2012 saschpe@suse.de
- Update to version 1.2.1:
  + Correct nose.__version__ (#549). Thanks to Chris Withers for the bug report.
- Changes from version 1.2.0:
  + Fixed issue where plugins included with `addplugins` keyword could
    be overridden by built-in plugins (or third-party plugins registered
    with setuptools) of the same name (#466).
  + Adds :option:`--cover-xml` and :option:`--cover-xml-file` (#311).
  + Adds support for :option:`--cover-branches` (related to #370).
  + Fixed Unicode issue on Python 3.1 with coverage (#442)
  + fixed class level fixture handling in multiprocessing plugin
  + Clue in the ``unittest`` module so it no longer prints traceback frames for
    our clones of their simple assertion helpers (#453). Patch by Erik Rose.
  + Stop using the ``assert`` statement in ``ok_`` and ``eq_`` so they work under
    ``python -O`` (#504). Patch by Erik Rose.
  + Add loglevel option to logcapture plugin (#493).
  + Add doctest options flag (#7 from google code tracker).
  + Add support for using 2to3 with the nosetests setuptools command.
  + Add --cover-min-percentage flag to force test runs without sufficient
    coverage to fail (#540). Patch by Domen Kožar.
  + Add travis-ci configuraion (#545).
  + Call reactor.stop from twisted thread (#301).
- Changes from version 1.1.2:
  + Fixed regression where the .coverage file was not saved (#439).
- Testsuite seems to work on SLE_11_SP2, reenable
- Symlink nosetests.1 manpage to nosetests-%%{python_version}.1
* Fri May 25 2012 toddrme2178@gmail.com
- Added python 3 documentation package
* Fri Apr 27 2012 toddrme2178@gmail.com
- Fix building python 3 package on openSUSE 11.4
* Thu Apr 26 2012 toddrme2178@gmail.com
- Add python 3 packages
* Tue Apr 24 2012 saschpe@suse.de
- Disable testsuite on openSUSE-11.4 and less to fix build
* Mon Apr  2 2012 saschpe@suse.de
- Move doc package into seperate spec to break build cycle between
  python-nose and python-Pygments (pulled in by python-Sphinx)
* Sat Mar 10 2012 saschpe@gmx.de
- Simply macro usage
- Run testsuite
* Wed Sep 21 2011 saschpe@suse.de
- Needs python-distribute at runtime
* Tue Sep 13 2011 saschpe@suse.de
- Upper-case %%description
* Thu Sep  8 2011 saschpe@suse.de
- Disabled testsuite to fix build
* Thu Sep  8 2011 saschpe@suse.de
- Update to 1.1.2:
  * Fixed regression where the .coverage file was not saved (#439).
  * Fixed missing nose.sphinx module in source distribution (#436).
- Spec file changes:
  * Depend on python-distribute instead of python-setuptools
  * Changed license to LGPL-2.0+ (SPDX style)
  * Properly build and install HTML documentation
* Mon Feb  7 2011 lars@linux-schulserver.de
- update to 1.0.0:
  + Made nose compatible with python 3.
  * *Huge** thanks to Alex "foogod" Stewart!
* Tue Sep 14 2010 coolo@novell.com
- update to 0.11.4
  - Made nose compatible with Python 2.7.
  - Fixed default plugin manager's use of plugin overriding. Thanks to
  rob.daylife for the bug report and patch. (#323).
  - Changed plugin loading so that external plugins loaded via extension
  points can override builtin plugins with the same name.
  ... for more see CHANGELOG
* Wed Jul 22 2009 lars@linux-schulserver.de
- update to 0.11.1
  + Fixed bug in xunit plugin xml escaping.
  + Fixed bug in xunit plugin that could cause test run to crash
    after certain types of errors or actions by other plugins.
  + Fixed bug in testid plugin that could cause test run to crash
    after certain types of errors or actions by other plugins.
  + Fixed bug in collect only plugin that caused it to fail when
    collecting from test generators.
  + Fixed some broken html in docs.
- update to 0.11.1 contains changes from 0.11:
  + Added multiprocess plugin that allows tests to be run in parallel
    across multiple processes.
  + Added logcapture plugin that captures logging messages and prints
    them with failing tests.
  + Added optional HTML coverage reports to coverage plugin.
  + Added plugin that enables collection of tests in all modules.
  + Added --failed option to testid plugin. When this option is in
    effect, if any tests failed in the previous test run (so long as
    testid was active for that test run) only the failed tests will run.
  + Made it possible to 'yield test' in addition to 'yield test,' from
    test generators.
  + Fixed bug that caused traceback inspector to fail when source code
    file could not be found.
  + Fixed some issues limiting compatibility with IronPython.
  + Added support for module and test case fixtures in doctest files.
  + Added --traverse-namespace commandline option that restores old
    default behavior of following all package __path__ entries when
    loading tests from packages.
  + Added --first-package-wins commandline option to better support
    testing parts of namespace packages.
  + Added versioned nosetests scripts (#123).
  + Fixed bug that would cause context teardown to fail to run in some
    cases.
  + Enabled doctest plugin to use variable other than "_" as the default
    result variable.
  + Fixed bug that would cause unicode output to crash output capture.
  + Added setUp and tearDown as valid names for module-level fixtures.
  + Fixed bug in list of valid names for package-level fixtures.
  + Updated man page generation using hacked up manpage writer from
    docutils sandbox.
- fix some rpmlint warnings
* Tue Dec  2 2008 jfunk@funktronics.ca
- Update to 0.10.4
  - nose is now compatible with python 2.6.
- 0.10.3
  - Fixed bug in nosetests setup command that caused an exception to be raised
  if run with options. Thanks to Philip Jenvey for the bug report (#191).
  - Raised score of coverage plugin to 200, so that it will execute before
  default-score plugins, and so be able to catch more import-time code. Thanks
  to Ned Batchelder for the bug report and patch (#190).
- 0.10.2
  - nose now runs under jython (jython svn trunk only at this time). Thanks to
  Philip Jenvey, Pam Zerbinos and the other pycon sprinters (#160).
  - Fixed bugs in loader, default plugin manager, and other modules that
  caused plugin exceptions to be swallowed (#152, #155). Thanks to John J
  Lee for the bug report and patch.
  - Added selftest.py script, used to test a non-installed distribution of
  nose (#49). Thanks to Antoine Pitrou and John J Lee for the bug report and
  patches.
  - Fixed bug in nose.importer that caused errors with namespace
  packages. Thanks to Philip Jenvey for the bug report and patch (#164).
  - Fixed bug in nose.tools.with_setup that prevented use of multiple
  @with_setup decorators. Thanks to tlesher for the bug report (#151).
  - Fixed bugs in handling of context fixtures for tests imported into a
  package. Thanks to Gary Bernhardt for the bug report (#145).
  - Fixed bugs in handling of config files and config file options for plugins
  excluded by a RestrictedPluginManager. Thanks to John J Lee and Philip
  Jenvey for the bug reports and patches (#158, #166).
  - Updated ErrorClass exception reporting to be shorter and more clear. Thanks
  to John J Lee for the patch (#142).
  - Allowed plugins to load tests from modules starting with '_'. Thanks to John
  J Lee for the patch (#82).
  - Updated documentation about building as rpm (#127).
  - Updated config to make including executable files the default on
  IronPython as well as on Windows. Thanks to sanxiyn for the bug
  report and patch (#183).
  - Fixed a python 2.3 incompatibility in errorclass_failure.rst
  (#173). Thanks to Philip Jenvey for the bug report and patch.
  - Classes with metaclasses can now be collected as tests (#153).
  - Made sure the document tree in the selector plugin test is accurate
  and tested (#144). Thanks to John J Lee for the bug report and
  patch.
  - Fixed stack level used when dropping into pdb in a doctest
  (#154). Thanks to John J Lee for the bug report and patch.
  - Fixed bug in ErrorClassPlugin that made some missing keyword
  argument errors obscure (#159). Thanks to Philip Jenvey for the bug
  report and patch.
* Mon Nov 10 2008 cfarrell1980@gmail.com
- try building with --record-rpm instead of --record as per bnc#441794
* Wed Jul  9 2008 poeml@suse.de
- fix build, the man page wasn't found.
* Tue Mar 18 2008 jfunk@funktronics.ca
- Update to 0.10.1:
  - Fixed bug in capture plugin that caused it to record captured output on the
  test in the wrong attribute (#113)
  - Fixed bug in result proxy that caused tests to fail if they accessed
  certain result attibutes directly (#114). Thanks to Neilen Marais for the
  bug report
  - Fixed bug in capture plugin that caused other error formatters changes to
  be lost if no output was captured (#124). Thanks to someone at ilorentz.org
  for the bug report
  - Fixed several bugs in the nosetests setup command that made some options
  unusable and the command itself unusable when no options were set (#125,
  [#126], #128). Thanks to Alain Poirier for the bug reports
  - Fixed bug in handling of string errors (#130). Thanks to schl... at
  uni-oldenburg.de for the bug report
  - Fixed bug in coverage plugin option handling that prevented
  - -cover-package=mod1,mod2 from working (#117). Thanks to Allen Bierbaum for
  the patch
  - Fixed bug in profiler plugin that prevented output from being produced when
  output capture was enabled on python 2.5 (#129). Thanks to James Casbon for
  the patch
  - Fixed bug in adapting 0.9 plugins to 0.10 (#119 part one). Thanks to John J
  Lee for the bug report and tests
  - Fixed bug in handling of argv in config and plugin test utilities (#119
  part two). Thanks to John J Lee for the bug report and patch
  - Fixed bug where Failure cases due to invalid test name specifications were
  passed to plugins makeTest (#120). Thanks to John J Lee for the bug report
  and patch
  - Fixed bugs in doc css that mangled display in small windows. Thanks to Ben
  Hoyt for the bug report and Michal Kwiatkowski for the fix
  - Made it possible to pass a list or comma-separated string as defaultTest to
  main(). Thanks to Allen Bierbaum for the suggestion and patch
  - Fixed a bug in nose.selector and nose.util.getpackage that caused
  directories with names that are not legal python identifiers to be
  collected as packages (#143). Thanks to John J Lee for the bug report
* Mon Jul  3 2006 judas_iscariote@shorewall.net
- update
* Mon Jul  3 2006 jfunk@funktronics.ca
- Initial release
