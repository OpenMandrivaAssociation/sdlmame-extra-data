Name:			sdlmame-extra-data
Version:		0.142u4
Release:		%mkrel 1

Summary:	More data files for SDL MAME front-ends
License:	Freeware
Group:		Emulators
URL:		http://mameworld.info/
# See "Support Files"

# Cheats (XML format)
Source1:	http://cheat.retrogames.com/download/cheat0142.zip
#alt url: http://www.mamecheat.co.uk/

# nplayers.ini
Source10:	http://nplayers.arcadebelgium.be/files/nplayers0142.zip

# history.dat
Source20:	http://www.arcade-history.com/dats/mamehistory142.7z

# mameinfo.dat
Source30:	http://www.mameworld.info/mameinfo/download/Mameinfo0142u4.zip

# catver.ini (en, fr, it)
# http://www.progettoemma.net/public/ccount/click.php?id=6
# http://clrmamepro.free.fr/file/catlist/catver.zip
# http://www.progettoemma.net/public/ccount/click.php?id=5
Source40:	catver-0.142u4-en.zip
Source41:	catver-0.142u4-fr.zip
Source42:	catver-0.142u4-it.zip

# controls.ini (for wahcade)
Source50:	controls.ini.0.111.5.zip

#"Art files" : samples, cabinets, etc...
#Source100:	http://www.mame.net/roms/gridlee-sample.zip

# for free, but for non-commercial use only
# from http://mamedev.org/roms/
# to add a rom archive : add its basename to the freerom_sources list below
#define freerom_sources "alienar carpolo circus crash fireone gridlee ripcord\
# robby robotbwl sidetrac spectar starfir2 starfira starfire targ teetert"
# this generates Source5xx tags
#(echo %{freerom_sources} | awk 'BEGIN { RS=" "; n=0 }; { print "Source"500+n":\t"$1".zip"; n++ };')
# this generates the list of rom files for the install step
#define freerom_files %(echo %{freerom_sources} | awk 'BEGIN { RS=" "; files="" }; { files=files" %{_sourcedir}/"$1".zip"}; END { print files };')
#TODO:
#1. obtain permission to distribute these roms,
#2. find and package all additionnal files related to these free roms,
#3. uncomment sources, update description, install, files...

BuildRequires:	p7zip
BuildRequires:	recode
BuildRequires:	perl

BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

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
7za e Mameinfo*.exe mameinfo.dat

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
 %{buildroot}/%{_gamesdatadir}/sdlmame/

#freeware roms
#install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame/roms
#install -m 644 %{freerom_files} %{buildroot}%{_gamesdatadir}/sdlmame/roms

%files
%defattr(-,root,root)
%{_gamesdatadir}/sdlmame/*

%clean
rm -rf %{buildroot}


