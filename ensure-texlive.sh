#!/bin/bash

PACKAGE_MANAGER=""

# Function to find the package manager
find_package_manager() {
    if command -v apt-get &> /dev/null; then
        echo "Package Manager: apt (Debian/Ubuntu-based)"
		PACKAGE_MANAGER=apt
    elif command -v yum &> /dev/null; then
        echo "Package Manager: yum (Older Red Hat/CentOS-based)"
		PACKAGE_MANAGER=yum
    elif command -v dnf &> /dev/null; then
        echo "Package Manager: dnf (Modern Red Hat/Fedora-based)"
		PACKAGE_MANAGER=dnf
    elif command -v pacman &> /dev/null; then
        echo "Package Manager: pacman (Arch Linux-based)"
		PACKAGE_MANAGER=pacman
    elif command -v zypper &> /dev/null; then
        echo "Package Manager: zypper (OpenSUSE-based)"
		PACKAGE_MANAGER=zypper
    elif command -v apk &> /dev/null; then
        echo "Package Manager: apk (Alpine Linux-based)"
		PACKAGE_MANAGER=apk
    elif command -v brew &> /dev/null; then
        echo "Package Manager: brew (MacOS-based)"
		PACKAGE_MANAGER=brew
    elif command -v choco &> /dev/null; then
        echo "Package Manager: chocolatey (Windows-based)"
		PACKAGE_MANAGER=choco
    else
        echo "Could not determine the package manager."
        return 1
    fi
    return 0
}

# Function to check for TeX Live installation
check_texlive() {
    if command -v pdflatex &> /dev/null; then
        echo "TeX Live (pdflatex) is installed."
        return 0
    elif command -v tex &> /dev/null; then
        echo "TeX Live (tex) is installed."
        return 0
    else
        echo "TeX Live does not appear to be installed."
        return 1
    fi
}

find_package_manager

if [[ ! -z $PACKAGE_MANAGER ]]; then
	if [[ ! check_texlive ]]; then
		sudo $PACKAGE_MANAGER texlive
	else
		echo "texlive looks like it's already installed."
	fi
fi
