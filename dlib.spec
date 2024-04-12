%global forgeurl https://github.com/davisking/dlib

Name:       dlib
Version:    19.24.4
Release:    %autorelease
Summary:    A modern C++ toolkit containing machine learning algorithms
%forgemeta
License:    BSL-1.0
URL:        http://dlib.net
Source:     %forgesource

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  cmake(pybind11)
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
# BLAS and LAPACK support
BuildRequires:  pkgconfig(flexiblas)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(x11)

# Failed to build to ppc64le
# Stop building for i686
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    ppc64le %{ix86}

%description
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. Its design is heavily influenced by ideas from
design by contract and component-based software engineering. It contains
components for dealing with networking, threads, graphical user interfaces,
data structures, linear algebra, machine learning, image processing, data
mining, XML and text parsing, numerical optimization, Bayesian networks, and
numerous other tasks.


%package devel
Summary:    Development files for dlib
License:    Boost and Public Domain
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains development files for
the library.


%package -n python3-%{name}
Summary:    Python 3 interface to %{name}
License:    Boost and Public Domain

%description -n python3-%{name}
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains Python 3 API for the
library.


%package doc
Summary:    Documentation for dlib
License:    Boost and Public Domain and CC-BY-SA
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description doc
Dlib is a general purpose cross-platform open source software library written
in the C++ programming language. This package contains the library
documentation and examples.


%prep
%forgeautosetup -p1

find docs -type f -exec chmod 644 {} +
find examples -type f -exec chmod 644 {} +

# unbundle pybind11, see https://bugzilla.redhat.com/2098694
rm -r dlib/external/pybind11
sed -i 's@add_subdirectory(../../dlib/external/pybind11 pybind11_build)@find_package(pybind11 CONFIG)@' tools/python/CMakeLists.txt


%generate_buildrequires
%pyproject_buildrequires


%build
%cmake
%cmake_build

%pyproject_wheel


%install
%cmake_install

rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{_docdir}/%{name}/LICENSE.txt
# Remove Sphinx build leftovers
rm -f %%{buildroot}/%{_docdir}/%{name}-doc/docs/python/.buildinfo

%pyproject_install
%pyproject_save_files -l %{name}

find %{buildroot} -name '.*' -exec rm -rf {} +


%files
%license dlib/LICENSE.txt
%{_libdir}/libdlib.so.19*

%files devel
%{_libdir}/libdlib.so
%{_includedir}/dlib/
%{_libdir}/cmake/dlib/
%{_libdir}/pkgconfig/*.pc

%files -n python3-%{name} -f %{pyproject_files}
%{python3_sitearch}/_%{name}_pybind11%{python3_ext_suffix}
%doc README.md

%files doc
%license examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt
%license examples/video_frames/license.txt
#%%doc documentation.html
%doc docs
#%%doc docs/python/_static/{jquery,underscore}.js
%doc examples


%changelog
%autochangelog
