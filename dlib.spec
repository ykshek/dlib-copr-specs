Name:		dlib
Version:	18.18
Release:	2%{?dist}
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
BuildRequires:	python2-devel
BuildRequires:	python3-devel

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


%package -n python2-%{name}
Summary:	Python 2 interface to %{name}
License:	Boost and Public Domain
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains Python 2 API for the
library.


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

%define setup_py_extra_opts --no USE_SSE4_INSTRUCTIONS
%py2_build %{setup_py_extra_opts}
%py3_build %{setup_py_extra_opts}


%install
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}
install -m 755 build/libdlib.so.%{version}.* %{buildroot}%{_libdir}
cp -a build/libdlib.so %{buildroot}%{_libdir}
find dlib -type f -name '*.h' -exec \
    install -D -m 644 {} %{buildroot}%{_includedir}/{} \;
%py2_install
%py3_install
find %{buildroot}%{python2_sitearch}/dlib/ -type f -name '*.py' -exec sed -i '1s|^#!.*|#!%{__python2}|' {} \;
find %{buildroot}%{python3_sitearch}/dlib/ -type f -name '*.py' -exec sed -i '1s|^#!.*|#!%{__python3}|' {} \;


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license dlib/LICENSE.txt
%{_libdir}/libdlib.so.*

%files devel
%{_libdir}/libdlib.so
%{_includedir}/dlib/

%files -n python2-%{name}
%license dlib/LICENSE.txt
%license python_examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%{python2_sitearch}/dlib/
%{python2_sitearch}/dlib-*.egg-info/

%files -n python3-%{name}
%license dlib/LICENSE.txt
%license python_examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%{python3_sitearch}/dlib/
%{python3_sitearch}/dlib-*.egg-info/

%files doc
%license examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%license examples/video_frames/license.txt
%doc documentation.html
%doc docs
%doc examples
%exclude %{_docdir}/%{name}-doc/docs/python/.doctrees
%exclude %{_docdir}/%{name}-doc/docs/python/.buildinfo


%changelog
* Sat Jan 23 2016 Dmitry Mikhirev <mikhirev@gmail.com> 18.18-2
- Rebuild against new libboost_python

* Wed Nov 4 2015 Dmitry Mikhirev <mikhirev@gmail.com> 18.18-1
- Initial package
