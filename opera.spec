AutoReqProv: no
%global debug_package %{nil}


%ifarch x86_64
%global arch amd64
%global fearch x86_64
%else
%global arch i386
%global fearch i386
%endif

%define deb_opera %{name}-stable_%{version}_%{arch}.deb

Summary: A fast and secure web browser
Name: opera
Version: 46.0.2597.39
Release: 1%{dist}
License: Proprietary
Group: Applications/Internet
URL: http://www.opera.com/
# You can download the latest opera source with the opera-snapshot.sh
Source0: http://get.geo.opera.com.global.prod.fastly.net/pub/%{name}/desktop/%{version}/linux/%{deb_opera}
Source1: opera-snapshot.sh
Patch:	 extraffmpeg.patch
Patch1:  widevine.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: systemd-libs
#Requires: libudev0
Requires: openssl1
Requires: gtk2
Requires: desktop-file-utils
Requires: shared-mime-info
Requires: libXtst
Requires: GConf2
Requires: curl
Requires: libXScrnSaver
Requires: glibc
Requires: alsa-lib
Requires: nss
Requires: freetype
Requires: chromium-freeworld-libs-media
BuildRequires: binutils xz tar systemd-libs wget curl 
Obsoletes: opera-stable
Conflicts: opera-beta opera-next opera-developer
Recommends: chromium-pepper-flash chromium-widevine

%description
Opera is a browser with innovative features, speed and security. 
The browser delivers a highly customizable start page (Speed Dial) 
where you can set your top sites and bookmarks, Off-road mode for 
data saving and faster browsing in slow networks such as 3G/2G and 
public Wi-Fi, a "Discover" page for getting the best of the web's 
content; and in the desktop version Stash, a tool for comparing 
pages and "read it later".

%prep

# extract data from the deb package
install -dm 755 %{_builddir}/%{name}-%{version}
ar x %{SOURCE0} 
if [ -f data.tar.xz ]; then
tar xJf data.tar.xz -C %{_builddir}/%{name}-%{version}
elif [ -f data.tar.gz ]; then 
tar xmzvf data.tar.gz -C %{_builddir}/%{name}-%{version}
fi

%setup -T -D %{name}-%{version} 
pushd usr/lib/%{fearch}-linux-gnu/opera/resources/
%patch -p0
%patch1 -p0 
popd 

%build


%install

# Make destiny directories
install -dm 755 %{buildroot}/%{_libdir} \
%{buildroot}/%{_bindir} 

# rename libdir
mv -f usr/lib/%{fearch}-linux-gnu/%{name} %{buildroot}/%{_libdir}/
mv -f usr/share %{buildroot}/%{_prefix}


echo '#!/bin/bash
if [ `getconf LONG_BIT` = "64" ]; then
libdir=/usr/lib64
else
libdir=/usr/lib
fi

cd $libdir/opera
LD_LIBRARY_PATH=$libdir:$libdir/opera:$libdir/opera/resources/ $libdir/opera/opera "$@" ' >> %{buildroot}/%{_bindir}/%{name}

chmod a+x %{buildroot}/%{_bindir}/%{name} 


# delete some directories that is not needed on Fedora
rm -rf %{buildroot}/%{_datadir}/{lintian,menu}

# correct opera_sandbox permission
# FATAL:setuid_sandbox_client.cc(283)] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now. You need to make sure that /usr/lib64/opera-developer/opera_sandbox is owned by root and has mode 4755.
chmod 4755 $RPM_BUILD_ROOT%{_libdir}/%{name}/opera_sandbox

# H264
rm -f %{buildroot}/%{_libdir}/%{name}/libffmpeg.so
ln -sf %{_libdir}/chromium/libffmpeg.so %{buildroot}/%{_libdir}/%{name}/libffmpeg.so

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/opera.desktop
%{_docdir}/opera-stable/
%{_datadir}/icons/hicolor/*/apps/opera.png
%{_datadir}/pixmaps/opera.xpm
%{_datadir}/mime/packages/opera-stable.xml



%changelog

* Thu Jul 06 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 46.0.2597.39-1
- Updated to 46.0.2597.39

* Thu Jun 29 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 46.0.2597.32-1
- Updated to 46.0.2597.32

* Tue Jun 13 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 45.0.2552.898-1
- Updated to 45.0.2552.898

* Sat Jun 10 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 45.0.2552.888-1
- Updated to 45.0.2552.888-1

* Tue May 30 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 45.0.2552.881-1
- Updated to 45.0.2552.881

* Sat Apr 08 2017 David Vásquez <davidva AT tutanota DOT com> - 44.0.2510.1159-1
- Updated to 44.0.2510.1159

* Sat Mar 25 2017 David Vásquez <davidva AT tutanota DOT com> - 44.0.2510.857-1
- Updated to 44.0.2510.857-1

* Fri Feb 17 2017 David Vásquez <davidva AT tutanota DOT com> - 43.0.2442.806-1
- Updated to 43.0.2442.806-1
- Support h264

* Fri Jan 13 2017 David Vásquez <davidva AT tutanota DOT com> - 42.0.2393.94-2
- Support chromium-widevine

* Thu Jan 12 2017 David Vásquez <davidva AT tutanota DOT com> - 42.0.2393.94-1
- Updated to 42.0.2393.94

* Tue Sep 20 2016 David Vásquez <davidva AT tutanota DOT com> - 40.0.2308.54-1
- Updated to 40.0.2308.54

* Mon Sep 19 2016 David Vásquez <davidva AT tutanota DOT com> - 39.0.2256.71-1
- Updated to 39.0.2256.71

* Wed Aug 10 2016 David Vásquez <davidva AT tutanota DOT com> - 39.0.2256.48-1
- Updated to 39.0.2256.48

* Sat Jul 16 2016 David Vásquez <davidva AT tutanota DOT com> - 38.0.2220.41-1
- Updated to 38.0.2220.41

* Tue Jun 14 2016 David Vásquez <davidva AT tutanota DOT com> - 38.0.2220.31-1
- Updated to 38.0.2220.31

* Tue Jun 07 2016 David Vásquez <davidva AT tutanota DOT com> - 38.0.2220.29-1
- Updated to 38.0.2220.29

* Sun May 08 2016 David Vásquez <davidva AT tutanota DOT com> - 37.0.2178.32-1
- Updated to 37.0.2178.32

* Thu Apr 14 2016 David Vásquez <davidva AT tutanota DOT com> - 36.0.2130.65-1
- Updated to 36.0.2130.65

* Tue Feb 02 2016 David Vásquez <davidva AT tutanota DOT com> - 35.0.2066.37-1
- Updated to 35.0.2066.37

* Wed Jan 27 2016 David Vásquez <davidva AT tutanota DOT com> - 34.0.2036.50-1
- Updated to 34.0.2036.50

* Thu Jan 07 2016 David Vásquez <davidva AT tutanota DOT com> - 34.0.2036.25-1
- Updated to 34.0.2036.25

* Fri Nov 06 2015 David Vásquez <davidva AT tutanota DOT com> - 33.0.1990.58-2
- Recommended chromium-pepper-flash

* Thu Nov 05 2015 David Vásquez <davidva AT tutanota DOT com> - 33.0.1990.58-1
- Updated to 33.0.1990.58

* Wed Sep 30 2015 David Vásquez <davidva AT tutanota DOT com> - 32.0.1948.69-1
- Updated to 32.0.1948.69

* Sat Aug 08 2015 David Vásquez <davidva AT tutanota DOT com> - 31.0.1889.99-1
- Updated to 31.0.1889.99

* Thu Jun 25 2015 David Vásquez <davidva AT tutanota DOT com> - 30.0.1835.88-1
- Updated to - 29.0.1795.60

* Sat May 23 2015 David Vásquez <davidva AT tutanota DOT com> - 29.0.1795.60-1
- Updated to - 29.0.1795.60
- Deleted bundled libraries (ssl)
- Rewrited spec, for future compatibility of Opera 32bits

* Wed Mar 18 2015 David Vásquez <davidva AT tutanota DOT com> - 28.0.1750.48-1
- Updated to - 28.0.1750.48-1

* Wed Jan 28 2015 David Vásquez <davidva AT tutanota DOT com> - 27.0.1689.54-1
- Updated to 27.0.1689.54

* Sat Jan 10 2015 David Vásquez <davidva AT tutanota DOT com> - 26.0.1656.60-1
- Upstream
- Updated to 26.0.1656.60
- replaced libudev.so.0 symlink for libudev0
- Added snapshot, it will download the current Opera deb version.

* Wed Oct 22 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 26.0.1655.0-2
- delete post and postun section
- install libudev.so.0 symlink in install section
