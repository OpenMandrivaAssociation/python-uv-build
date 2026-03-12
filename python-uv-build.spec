%undefine _debugsource_template
%define module uv-build
%define oname uv_build

Name:		python-uv-build
Version:	0.10.9
Release:	1
Summary:	The uv-build backend
Group:		Development/Python
License:	MIT OR Apache-2.0
URL:		https://pypi.org/project/uv-build/
Source0:	https://files.pythonhosted.org/packages/source/u/%{oname}/%{oname}-%{version}.tar.gz
Source1:	%{oname}-%{version}-vendor.tar.xz

BuildSystem:	python
BuildRequires:  cargo
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:  rust-packaging

%description
This package is a cut down version of uv only providing the uv-build backend.

%prep
%autosetup -n %{oname}-%{version} -p1 -a1
# prep vendorered crates
%cargo_prep -v vendor/
# create .cargo/config file from vendoring output
cat >>.cargo/config <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build -p
export CARGO_HOME=$PWD/.cargo
# sort out crate licenses
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%files
%doc README.md
%license LICENSE-APACHE LICENSE-MIT LICENSES.dependencies
%{_bindir}/uv-build
%{python_sitearch}/%{oname}
%{python_sitearch}/%{oname}-%{version}.dist-info
