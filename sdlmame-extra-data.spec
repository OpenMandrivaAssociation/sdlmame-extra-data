Name:		sdlmame-extra-data
Version:	0.145
Release:	2
Summary:	More data files for SDL MAME front-ends
License:	Freeware
Group:		Emulators
URL:		http://mameworld.info/

# Cheats (XML format)
Source1:	http://cheat.retrogames.com/download/cheat0145.zip
#alt url: http://www.mamecheat.co.uk/
# nplayers.ini
Source10:	http://nplayers.arcadebelgium.be/files/nplayers0145.zip
# history.dat
Source20:	http://www.arcade-history.com/dats/mamehistory145.7z
# mameinfo.dat
Source30:	http://www.mameworld.info/mameinfo/download/Mameinfo0145.zip
# catver.ini (en, fr, it)
# http://www.progettoemma.net/public/ccount/click.php?id=6
# http://clrmamepro.free.fr/file/catlist/catver.zip
# http://www.progettoemma.net/public/ccount/click.php?id=5
Source40:	catver-0.145-en.zip
Source41:	catver-0.145-fr.zip
Source42:	catver-0.145-it.zip
# controls.ini (for wahcade)
Source50:	controls.ini.0.111.5.zip

BuildRequires:	p7zip
BuildRequires:	recode
BuildRequires:	perl

BuildArch:	noarch

# cheat.zip does not require a front-end
Requires:	sdlmame

%description
This package includes additional files for SDL MAME arcade emulator, which
are used by sdlmame itself (cheat.zip) or its front-ends.

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}

#cheats
unzip %{SOURCE1}

#nplayers
unzip -CoLaa %{SOURCE10} nplayers.ini
perl -pe "s/([0-9])P/\$1J/g" nplayers.ini >nplayers-fr.ini

#history
7za x %{SOURCE20}

#mameinfo
unzip -o %{SOURCE30}
7za e Mameinfo*.7z mameinfo.dat

#catver
unzip -Coaap %{SOURCE40} Catver.ini >catver-en.ini
unzip -Coaap %{SOURCE41} Catver.ini >catver-fr.ini
unzip -Coaap %{SOURCE42} Catver.ini >catver-it.ini
#fix catver (for loemu)
recode l1..u8 catver-fr.ini catver-it.ini
perl -pi -e "s/^=/#=/g" catver-fr.ini

#controls
unzip -o %{SOURCE50}

%build

%install
cd %{name}-%{version}
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame
install -m 644 cheat.zip catver-en.ini catver-fr.ini catver-it.ini \
 controls.ini history.dat mameinfo.dat nplayers.ini nplayers-fr.ini \
 %{buildroot}%{_gamesdatadir}/sdlmame/

%files
%{_gamesdatadir}/sdlmame/*

%clean
rm -rf %{buildroot}


