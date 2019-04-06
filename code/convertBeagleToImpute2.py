"""
Author: Shyam Gopalakrishnan
Date:   18th February 2019
Verion: 1.0

This script is used to convert a beagle imputation panel to impute2 format. 
"""

import argparse
import sys

def parse_args():
    """Parse command line args.

    This function parses the input arguments and 
    returns an object with them.
    
    Returns
    -------
    args : namespace
        Contains parsed command line arguments.
    
    """
    parser = argparse.ArgumentParser("Reference panel converter", version="1.0")
    parser.add_argument
