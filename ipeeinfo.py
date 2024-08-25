#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Kourva
# Source: https://github.com/Kourva/IpeeInfo

# IpeeInfo  is a   top-of-the-line IP  information tool
#   that boasts a   wide range  of features to help you
#   gain insight into any IP address.  Whether   you're
#   looking for the  geolocation of a  specific IP, its
#   latitude   and longitude   coordinates, or the city
#   it's based in, iPeeInfo has got you covered.

# What sets  iPeeInfo  apart from  other IP information
#    tools  is its  versatility. With  its command-line
#    interface, you  can  easily   specify  multiple IP
#    addresses to be scanned at once, making it perfect
#    for  network  administrators   who need  to gather
#    information about   large numbers of IP  addresses
#    quickly.  Additionally,  iPeeInfo  allows   you to
#    choose  between three  different   output  formats
#    (text, JSON, or CSV),  so you  can customize  your
#    output depending on your needs.

# But that's not all - iPeeInfo also includes an option
#    to save the results of your scan,  allowing you to
#    refer back to them later   if needed. This feature
#    is particularly  useful if you're performing scans
#    on a regular  basis and need to keep track of your
#    findings.

# Overall, iPeeInfo   is  a powerful   and  reliable IP
#    information tool  that is easy   to use and packed
#    with    features. Whether   you're a   seasoned IT
#    professional   or new to the field, iPeeInfo is an
#    essential tool for anyone who needs to gather data
#    about IP addresses.


# Libraries   (All  are built-in)  (No need to install)
#    anything with pip package installer
import threading
import itertools
import requests
import argparse
import logging
import time
import json
import sys
import os


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Colors
org = "\033[0;33;40m"  # Orange
wht = "\033[0;37;40m"  # White
grn = "\033[0;32;40m"  # Green
red = "\033[0;31;40m"  # Red
rst = "\033[m"         # Reset


# Ip search function
def ip_to_location(target, ipformat="text", output=None):

    """
    IP search function that retrieves the location data for  a
    given IP address.

    :param target: 
        The target IP address to search for.
    
    :param ipformat: 
        The desired format for the output (text, json, or csv)
        Default is 'text'.
    
    :param output: 
        Optional   output file   path. If provided, the result 
        will be saved to this file.

    :returns: 
        If no output file path is provided, the result will be 
        printed    to  the  console.  Otherwise,  the   result
        will   be saved   to the specified  output   file path.
    """

    # Make request with session to API
    with requests.Session() as session:
        response = session.get(
            f"https://freeipapi.com/api/json/{target}", stream=True, timeout=10
        ).json()

    # Extract relevant fields from response
    ipAddress = response["ipAddress"]
    ipVersion = response["ipVersion"]
    latitude = response["latitude"]
    longitude = response["longitude"]
    countryCode = response["countryCode"]
    countryName = response["countryName"]
    timeZone = response["timeZone"]
    cityName = response["cityName"]
    regionName = response["regionName"]

    # Stop animation
    event.set()
    print()

    # Enter Statement if Format is Text (Default)
    if ipformat == "text":

        # Store output
        output_result = (
            f"{org} |\n{org}[*] General Info\n {org}|{rst}\n "
            f"{org}|--{rst} {wht}IP Address   :{rst}  {grn}{ipAddress}\n "
            f"{org}|--{rst} {wht}Version      :{rst}  {grn}{ipVersion}\n {org}|\n"
            f"[*] Geo Location\n {org}|{rst}\n {org}|--{rst} {wht}Latitude     :{rst}  "
            f"{grn}{latitude}\n {org}|--{rst} {wht}Longitude    :{rst}  {grn}{longitude}\n "
            f"{org}|  \n[*] Address Info\n {org}|{rst}\n {org}|--{rst} {wht}"
            f"Country code :{rst}  {grn}{countryCode}\n {org}|--{rst} {wht}"
            f"Country name :{rst}  {grn}{countryName}\n {org}|--{rst} {wht}"
            f"Time Zone    :{rst}  {grn}{timeZone}\n {org}|--{rst} {wht}"
            f"City name    :{rst}  {grn}{cityName}\n {org}|--{rst} {wht}"
            f"Region name  :{rst}  {grn}{regionName}\n\n\n"
        )

        # Print output if no save option requested
        if output == None:
            print(output_result)
            return

        # Otherwise save the result 
        else:
            with open(f"{os.getcwd()}/{ipAddress}.txt", "w") as out:
                out.write(
                    output_result.replace(org, "")
                    .replace(rst, "")
                    .replace(grn, "")
                    .replace(wht, "")
                )
            print(f"{org} |\n{org}[*] Saved to {os.getcwd()}/{ipAddress}.txt\n")
            return

    # Enter Statement if Format is json
    elif ipformat == "json":

        # Store output
        output_result = (
            f"{org} |\n{org}[*] Json Output {rst} "
            f"{grn}{json.dumps(response, indent=4)}{rst}"
            f"\n\n\n"
        )
        # Print output if no save option requested
        if output == None:
            print(output_result)
            return

        # Otherwise save the result 
        else:
            with open(f"{os.getcwd()}/{ipAddress}.json", "w") as out:
                out.write(
                    output_result.replace(f"{org} |\n{org}[*] Json Output {rst} ", "")
                    .replace(org, "")
                    .replace(rst, "")
                    .replace(grn, "")
                    .replace(wht, "")
                )
            print(f"{org} |\n{org}[*] Saved to {os.getcwd()}/{ipAddress}.json\n")
            return

    # Enter Statement if Format is csv
    elif ipformat == "csv":

        # Store output
        output_result = (
            f"{org}ipAddress,ipVersion,latitude,longitude,countryCode,countryName,timeZone,cityName,regionName{rst}\n"
            f"{grn}{ipAddress},{ipVersion},{latitude},{longitude},{countryCode},{countryName},{timeZone},{cityName},{regionName}{rst}\n"
        )

        # Print output if no save option requested
        if output == None:
            print(output_result)
            return

        # Otherwise save the result 
        else:
            with open(f"{os.getcwd()}/{ipAddress}.csv", "w") as out:
                out.write(
                    output_result.replace(org, "").replace(rst, "").replace(grn, "")
                )
            print(f"{org} |\n{org}[*] Saved to {os.getcwd()}/{ipAddress}.csv\n")
            return


# Define the thread event variable (Used to stop thread)
event = threading.Event()


# Function to animate loading prompt
def animate_loading():

    # Animation actions
    sequence = ["-", "/", "|", "\\"]
    dots = [".   ", "..  ", "... ", "...."]

    # Cycle between all indexes of two lists
    for char, dot in itertools.cycle(zip(sequence, dots)):

        # Stop thread when we set even
        if event.is_set():
            break
        print(f"\r{org}[{char}]{rst} {wht}Searching {dot}{rst}", end="")
        time.sleep(0.5)


# Main Function
def ipeeinfo(ipaddr=[], ipformat="text", output=None):

    """
    This function takes an IP address as input  and  retrieves 
    information  about the  location of  that IP address using 
    the ip_to_location function. 

    :param ipaddr: 
        A  list or  string containing one or more IP addresses 
        to retrieve information for.
        If not provided, the user will be prompted to enter  a 
        target IP address.

    :param ipformat: 
        The format in which to retrieve the IP location   data
        (default is "text").

    :param output: 
        The file path to save the retrieved  IP location  data 
        to (default is None).

    :return: 
        None, but the retrieved IP   location data   will   be
        printed to the console and/or saved to a file.
    """

    # Get target from input if there is no argument Ip address
    if ipaddr == []:
        target = input(f"{org}[?]{rst} {wht}Enter Target IP Address:{rst} {org}")
        print(f" |{rst}")
        ipaddr.append(target)

    # Otherwise use argument IP(s)
    else:
        target = ipaddr

    # Get Information of target(s) for each
    for target in ipaddr:
        print(f"{org}[*] IpeeInfo: Starting Process!")

        # Create animation thread
        animation = threading.Thread(target=animate_loading, daemon=True)

        # Try to get Info
        try:
            print(f"{org} |  {rst}")
            event.clear()
            animation.start()

            # Call Ip to location function for each IP
            response = ip_to_location(target, ipformat, output)

        # Error Handling and Keyboard Interrupt
        except Exception as ex:
            logger.info(f"\n{org} |  {rst}\n{red}[x] Error: {ex!r}{rst}", exc_info=True)
        except KeyboardInterrupt:
            logger.info(f"\n{org} |  {rst}\n{red}[x] Exit code requested by user.{rst}")
            sys.exit()


# Set the arguments and run the main function
if __name__ == "__main__":

    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="Powerful Ip Info Script made in Python"
    )

    # Add options to parser
    # Option 1 -> Ip option
    parser.add_argument(
        "ip", 
        nargs="*", 
        help="iP address(es) to lookup"
    )

    # Option 2 -> format option
    parser.add_argument(
        "-f",
        choices=["text", "json", "csv"],
        default="text",
        help="output format (text or json or csv)"
    )

    # Option 3 -> save option
    parser.add_argument(
        "-o", 
        action="store_true",
        help="save result(s) of scan"
    )

    # Set the arguments
    args = parser.parse_args()


    # Handle arguments
    if args.ip:
        ip_args = [args.ip]
    else:
        ip_args = []

    output_format = args.f or "text"
    output_path = args.o or None

    ipeeinfo(ip_args, output_format, output_path)
