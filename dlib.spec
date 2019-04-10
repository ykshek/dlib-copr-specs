Name:		dlib
Version:	19.17
Release:	1%{?dist}
Summary:	A modern C++ toolkit containing machine learning algorithms

License:	Boost
URL:		http://dlib.net
Source0:	http://dlib.net/files/%{name}-%{version}.tar.bz2

BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	libX11-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	gcc-gfortran
BuildRequires:	openblas-devel
BuildRequires:	sqlite-devel
BuildRequires:	fftw-devel
BuildRequires:	boost-devel
BuildRequires:	python3-devel
BuildRequires:	boost-python3-devel

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
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description doc
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains the library
documentation and examples.


%prep
%autosetup
find docs -type f -exec chmod 644 {} +
find examples -type f -exec chmod 644 {} +
mkdir -p build

%build
pushd build

%cmake ../dlib
%make_build

popd
# this is really needed: in the python tools build it's enabled by
# default and we do not want that. see
# https://github.com/davisking/dlib/commit/fbd117804758bd9174a27ce471acfe21b8bfc208
# and https://github.com/davisking/dlib/issues/111
%define py_setup_args --no USE_SSE4_INSTRUCTIONS
%py3_build


%install
pushd build
%make_install
popd
rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{_docdir}/dlib/LICENSE.txt

%py3_install
# Some files got ambiguous python shebangs, we fix them after everything else is done
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitearch}/

find %{buildroot} -name '.*' -exec rm -rf {} +

%files
%license dlib/LICENSE.txt
%{_libdir}/libdlib.so.*

%files devel
%{_libdir}/libdlib.so
%{_includedir}/dlib/
%{_libdir}/cmake/dlib/
%{_libdir}/pkgconfig/*.pc

%files -n python3-%{name}
%license dlib/LICENSE.txt
%license python_examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%{python3_sitearch}/dlib.cpython-37m-x86_64-linux-gnu.so
%{python3_sitearch}/dlib-*.egg-info/

%files doc
%license examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%license examples/video_frames/license.txt
%doc documentation.html
%doc docs
%doc examples

%changelog
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

