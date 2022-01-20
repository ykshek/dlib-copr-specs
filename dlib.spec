%global	majorver 22

Name:		dlib
Version:	19.%{majorver}
Release:	5%{?dist}
Summary:	A modern C++ toolkit containing machine learning algorithms

License:	Boost
URL:		http://dlib.net
Source0:	http://dlib.net/files/%{name}-%{version}.tar.bz2

BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:	python3-setuptools
# BLAS and LAPACK support
BuildRequires:	pkgconfig(flexiblas)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(x11)

# Failed to build to ppc64le
ExcludeArch:	ppc64le

%description
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. Its design is heavily influenced by ideas from
design by contract and component-based software engineering. It contains
components for dealing with networking, threads, graphical user interfaces,
data structures, linear algebra, machine learning, image processing, data
mining, XML and text parsing, numerical optimization, Bayesian networks, and
numerous other tasks.


%package devel
Summary:	Development files for dlib
License:	Boost and Public Domain
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains development files for
the library.


%package -n python3-%{name}
Summary:	Python 3 interface to %{name}
License:	Boost and Public Domain
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains Python 3 API for the
library.


%package doc
Summary:	Documentation for dlib
License:	Boost and Public Domain and CC-BY-SA
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains the library
documentation and examples.


%prep
%autosetup -p1
find docs -type f -exec chmod 644 {} +
find examples -type f -exec chmod 644 {} +

%build
%cmake
%cmake_build

# this is really needed: in the python tools build it's enabled by
# default and we do not want that. see
# https://github.com/davisking/dlib/commit/fbd117804758bd9174a27ce471acfe21b8bfc208
# and https://github.com/davisking/dlib/issues/111
%global py_setup_args --no USE_SSE4_INSTRUCTIONS
%py3_build


%install
%cmake_install

rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{_docdir}/%{name}/LICENSE.txt
# Remove Sphinx build leftovers
rm -f %%{buildroot}/%{_docdir}/%{name}-doc/docs/python/.buildinfo

%py3_install
# Some files got ambiguous python shebangs, we fix them after everything else is done
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitearch}/

find %{buildroot} -name '.*' -exec rm -rf {} +

%files
%license dlib/LICENSE.txt
%{_libdir}/libdlib.so.19*

%files devel
%{_libdir}/libdlib.so
%{_includedir}/dlib/
%{_libdir}/cmake/dlib/
%{_libdir}/pkgconfig/*.pc

%files -n python3-%{name}
%license dlib/LICENSE.txt
%license python_examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%{python3_sitearch}/_%{name}_pybind11%{python3_ext_suffix}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-*.egg-info/

%files doc
%license examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%license examples/video_frames/license.txt
%doc documentation.html
%doc docs
%doc docs/python/_static/{jquery,underscore}.js
%doc examples


%changelog
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 19.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Iñaki Úcar <iucar@fedoraproject.org> - 19.22-4
- Switch back to FlexiBLAS

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 19.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 19.22-2
- Rebuilt for Python 3.10

* Mon Mar 29 2021 Luya Tshimbalanga <luya@fedoraproject.org> - 19.22-1
- Update to 19.22
- Enable BLAS and LAPACK support

* Tue Feb 09 2021 Luya Tshimbalanga <luya@fedoraproject.org> - 19.21-1
- Update to 19.21

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 19.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 02 2020 Miro Hrončok <mhroncok@redhat.com> <luya@fedoraproject.org> - 19.20-7
- Changes/Python Upstream Architecture Names

* Mon Aug 10 2020 Iñaki Úcar <iucar@fedoraproject.org> - 19.20-6
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Mon Aug 03 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 19.20-5
- Use cmake macros for build and install

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.20-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 03 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 19.20-2
- Set noarch for large documentation package
- Use specific versioning for libraries
- Remove Sphinx build leftovers
- Use %%global instead of %%define for declaration

* Fri Jul 03 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 19.20-1
- Update to 19.20

* Wed Mar 06 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 19.17-1
- Update to 19.17

* Wed Mar 06 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 19.16-3
- Drop hard path buildrequires for python3 shebang fix

* Wed Nov 28 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 19.16-2
- Fix directory ownership

* Wed Nov 28 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 19.16-1
- Update to 19.16
- Drop ldconfig scripts
- Fix all python shebangs with new method

* Mon Sep 24 2018 Miro Hrončok <mhroncok@redhat.com> - 19.4-10
- Drop Python 2 subpackage (#1627444)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 19.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 19.4-8
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 19.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 19.4-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 19.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 19.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 19.4-3
- Rebuilt for Boost 1.64

* Sun May 21 2017 Dmitry Mikhirev <mikhirev@gmail.com> 19.4-2
- Add BR boost-python3-devel (RHBZ #1443250)

* Mon Apr 17 2017 Dmitry Mikhirev <mikhirev@gmail.com> 19.4-1
- Update to 19.4 (RHBZ #1442868)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 18.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 18.18-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18.18-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 18.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Dmitry Mikhirev <mikhirev@gmail.com> 18.18-2
- Rebuild against new libboost_python

* Wed Nov 4 2015 Dmitry Mikhirev <mikhirev@gmail.com> 18.18-1
- Initial package
