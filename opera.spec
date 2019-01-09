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
Version: 57.0.3098.116
Release: 2%{dist}
License: Proprietary
Group: Applications/Internet
URL: http://www.opera.com/
# You can download the latest opera source with the opera-snapshot.sh
Source0: http://get.geo.opera.com.global.prod.fastly.net/pub/%{name}/desktop/%{version}/linux/%{deb_opera}
Source1: opera-snapshot.sh
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
LD_LIBRARY_PATH=$libdir:$libdir/opera:$libdir/opera/resources/:$PWD $libdir/opera/opera "$@" ' >> %{buildroot}/%{_bindir}/%{name}

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

* Wed Jan 09 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 57.0.3098.116-2
- Updated to 57.0.3098.116

* Fri Jan 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 57.0.3098.110-2
- Updated to 57.0.3098.110

* Sat Dec 22 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 57.0.3098.106-2
- Updated to 57.0.3098.106

* Sat Dec 15 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 57.0.3098.102-2
- Updated to 57.0.3098.102

* Tue Dec 11 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 57.0.3098.91f-2
- Updated to 57.0.3098.91

* Wed Nov 28 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 57.0.3098.76-2
- Updated to 57.0.3098.76

* Wed Nov 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 56.0.3051.104-2
- Updated to 56.0.3051.104

* Thu Nov 08 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 56.0.3051.99-2
- Updated to 56.0.3051.99

* Mon Oct 22 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 56.0.3051.52-2
- Updated to 56.0.3051.52

* Wed Oct 10 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 56.0.3051.43-2
- Updated to 56.0.3051.43

* Thu Oct 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 56.0.3051.36-2
- Updated to 56.0.3051.36

* Wed Sep 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 56.0.3051.31-2
- Updated to 56.0.3051.31

* Fri Sep 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 55.0.2994.61-2
- Updated to 55.0.2994.61

* Fri Sep 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 55.0.2994.56-2
- Updated to 55.0.2994.56

* Thu Aug 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 55.0.2994.37-2
- Updated to 55.0.2994.37

* Tue Aug 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 54.0.2952.71-2
- Updated to 54.0.2952.71

* Wed Jul 25 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 54.0.2952.64-2
- Updated to 54.0.2952.64

* Thu Jul 19 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 54.0.2952.60-2
- Updated to 54.0.2952.60

* Fri Jul 13 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 54.0.2952.54-2
- Updated to 54.0.2952.54

* Sat Jul 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 54.0.2952.51-2
- Updated to 54.0.2952.51

* Thu Jul 05 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 54.0.2952.46-2
- Updated to 54.0.2952.46

* Thu Jun 28 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 54.0.2952.41-2
- Updated to 54.0.2952.41

* Tue Jun 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 53.0.2907.110-2
- Updated to 53.0.2907.110

* Sat Jun 23 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 53.0.2907.106-2
- Updated to 53.0.2907.106

* Sun Jun 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 53.0.2907.99-2
- Fix internal dependency

* Thu Jun 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 53.0.2907.99-1
- Updated to 53.0.2907.99

* Thu May 24 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 53.0.2907.68-1
- Updated to 53.0.2907.68

* Wed May 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 53.0.2907.57-1
- Updated to 53.0.2907.57

* Thu May 10 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 53.0.2907.37-1
- Updated to 53.0.2907.37

* Thu May 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 52.0.2871.99-1
- Updated to 52.0.2871.99

* Wed Apr 25 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 52.0.2871.97-1
- Updated to 52.0.2871.97

* Thu Apr 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 52.0.2871.64-1
- Updated to 52.0.2871.64

* Sat Mar 31 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 52.0.2871.40-1
- Updated to 52.0.2871.40

* Tue Mar 27 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 52.0.2871.37-1
- Updated to 52.0.2871.37

* Wed Mar 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 52.0.2871.30-1
- Updated to 52.0.2871.30

* Wed Mar 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 51.0.2830.55-1
- Updated to 51.0.2830.55

* Fri Feb 23 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 51.0.2830.40-1
- Updated to 51.0.2830.40

* Fri Feb 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 51.0.2830.34-1
- Updated to 51.0.2830.34

* Wed Feb 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 51.0.2830.26-1
- Updated to 51.0.2830.26

* Sun Jan 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 50.0.2762.67-1
- Updated to 50.0.2762.67

* Thu Jan 11 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 50.0.2762.58-1
- Updated to 50.0.2762.58

* Wed Jan 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 50.0.2762.45-1
- Updated to 50.0.2762.45

* Wed Dec 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 49.0.2725.64-1
- Updated to 49.0.2725.64

* Tue Dec 12 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 49.0.2725.56-1
- Updated to 49.0.2725.56

* Thu Nov 16 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 49.0.2725.39-1
- Updated to 49.0.2725.39

* Fri Nov 10 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 49.0.2725.34-1
- Updated to 49.0.2725.34

* Wed Oct 25 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 48.0.2685.52-1
- Updated to 48.0.2685.52

* Sun Oct 22 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 48.0.2685.50-1
- Updated to 48.0.2685.50

* Fri Oct 13 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 48.0.2685.39-1
- Updated to 48.0.2685.39

* Tue Oct 03 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 48.0.2685.35-1
- Updated to 48.0.2685.35

* Tue Sep 26 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 48.0.2685.32-1
- Updated to 48.0.2685.32

* Sat Sep 09 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 47.0.2631.80-1
- Updated to 47.0.2631.80

* Sun Aug 13 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 47.0.2631.39-1
- Updated to 47.0.2631.39

* Thu Jul 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 46.0.2597.57-1
- Updated to 46.0.2597.57

* Wed Jul 12 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 46.0.2597.46-1
- Updated to 46.0.2597.46

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
