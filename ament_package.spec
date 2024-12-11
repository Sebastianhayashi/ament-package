%bcond_without tests
%bcond_without weak_deps
%define debug_package %{nil}

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/usr/.*$
%global __requires_exclude_from ^/usr/.*$

Name:           ros-jazzy-ament-package
Version:        0.16.3
Release:        0%{?dist}%{?release_suffix}
Summary:        ROS ament_package package

License:        Apache License 2.0
Source0:        ros-jazzy-ament-package-0.16.3.tar.gz

Requires:       python3-importlib-metadata
Requires:       python3-importlib-resources
Requires:       python3-setuptools
BuildRequires:  python%{python3_pkgversion}-devel

%if 0%{?with_tests}
BuildRequires:  python3-flake8
BuildRequires:  python3-pytest
%endif

%description
The parser for the manifest files in the ament buildsystem.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/usr/setup.sh" ]; then . "/usr/setup.sh"; fi
%py3_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/usr/setup.sh" ]; then . "/usr/setup.sh"; fi
%py3_install -- --prefix "/usr"

%if 0%{?with_tests}
%check
# Look for a directory with a name indicating that it contains tests
TEST_TARGET=$(ls -d * | grep -m1 "\(test\|tests\)" ||:)
if [ -n "$TEST_TARGET" ] && %__python3 -m pytest --version; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/usr/setup.sh" ]; then . "/usr/setup.sh"; fi
%__python3 -m pytest $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/usr

%changelog
* Tue Dec 10 2024 Dharini Dutia <dharini@openrobotics.org> - 0.16.3-0
- Autogenerated by Bloom
