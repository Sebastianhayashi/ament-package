%bcond_without tests
%bcond_without weak_deps
%define debug_package %{nil}
%define ros_distro jazzy

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/opt/ros/%{ros_distro}/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/%{ros_distro}/.*$
%global __requires_exclude_from ^/opt/ros/%{ros_distro}/.*$

Name:           ros-jazzy-ament-package
Version:        0.16.3
Release:        0%{?dist}%{?release_suffix}
Summary:        ROS ament_package package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       python3-importlib-metadata
Requires:       python3-importlib-resources
Requires:       python3-setuptools
BuildRequires:  python%{python3_pkgversion}-devel

%if 0%{?with_tests}
BuildRequires:  python3-flake8
BuildRequires:  python3-pytest
BuildRequires: ros-jazzy-ament-package
%endif

%description
The parser for the manifest files in the ament buildsystem.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it. It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/%{ros_distro}/setup.sh" ]; then . "/opt/ros/%{ros_distro}/setup.sh"; fi
%py3_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it. It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/%{ros_distro}/setup.sh" ]; then . "/opt/ros/%{ros_distro}/setup.sh"; fi
%py3_install -- --prefix "/opt/ros/%{ros_distro}"

%if 0%{?with_tests}
%check
# 检查是否存在测试目录或文件
if [ -d "tests" ] || ls test_*.py *_test.py > /dev/null 2>&1; then
    %__python3 -m pytest tests || echo "RPM TESTS FAILED"
else
    echo "No tests to run, skipping."
fi
%endif

%files
/opt/ros/%{ros_distro}

%changelog
* Tue Dec 10 2024 Dharini Dutia <dharini@openrobotics.org> - 0.16.3-0
- Autogenerated by Bloom