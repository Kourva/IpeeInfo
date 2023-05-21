#!/bin/bash

# Function to check root access
check_root() {
    [[ $EUID -eq 0 ]]
}

# Check if ipeeinfo is already installed
check_installed() {
    [[ -f "/usr/bin/ipeeinfo" ]]
}

# Installing process
installer() {
    if check_installed; then
        # If package is already installed, print message and exit
        echo -e "\ninfo: ipeeinfo is already installed."
        exit 0
    fi

    # Print install message
    echo -e "\ninfo: installing package for you."

    # Copy file to /usr/bin
    if ! cp ipeeinfo.py /usr/bin/ipeeinfo; then
        echo "error: failed to copy file to /usr/bin"
        exit 1
    fi

    # Change permissions
    if ! chmod 755 /usr/bin/ipeeinfo; then
        echo "error: failed to set executable permission for /usr/bin/ipeeinfo"
        exit 1
    fi

    # Print success message
    echo "success: ipeeinfo has been installed."
}

# Uninstalling process
uninstaller() {
    # Print uninstall message
    echo -e "\ninfo: uninstalling package from your system."

    # Remove file from /usr/bin
    if check_installed; then
        if ! rm /usr/bin/ipeeinfo; then
            echo "error: failed to remove /usr/bin/ipeeinfo"
            exit 1
        fi

        # Print success message
        echo "success: ipeeinfo has been uninstalled."
    else
        # If package is not installed, print message and exit
        echo "info: ipeeinfo is not installed."
        exit 0
    fi
}

if check_root; then
    if [[ $# -gt 0 && "$1" == "--uninstall" ]]; then
        uninstaller
    else
        installer
    fi
else
    echo "error: you cannot perform this operation unless you are root."
    exit 1
fi