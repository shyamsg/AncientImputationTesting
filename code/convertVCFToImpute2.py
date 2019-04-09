"""This script is used to convert a beagle imputation panel to impute2 format.

Author:  Shyam Gopalakrishnan
Date:    18th February 2019
Version: 1.0
"""


import argparse
import gzip
import os


def parse_args():
    """Parse command line args.

    This function parses the input arguments and
    returns an object with them.

    Returns
    -------
    args : namespace
        Contains parsed command line arguments.

    """
    parser = argparse.ArgumentParser(description="Reference panel converter",
                                     version="1.0")
    parser.add_argument("-i", "--inputFile", help="Input in beagle format",
                        required=True)
    parser.add_argument("-p", "--partLength", type=int,
                        help="Number of SNPs in each part",
                        required=False, default=10000)
    parser.add_argument("-o", "--outPrefix", help="Out prefix",
                        default="")
    args = parser.parse_args()
    if args.outPrefix == "":
        args.outPrefix = os.path.splitext(args.inputFile)
    return(args)


def process_one_vcf_line(vcf_line, legend_file, haps, num_samples):
    """Process one non-header line from vcf.

    Process one line of a vcf file (non-header version). Write information to
    legend file and update the strings for the haps file.

    Parameters
    ----------
    vcf_line : string
        Line from vcf file
    legend_file : file handle
        Output file with snp information
    haps : list
        List of strings with each containing one haplotype
    num_samples : int
        Number of samples

    Raises
    ------
    ValueError
        when something is fishy about the vcf line.

    """
    vcf_toks = vcf_line.strip().split()
    if len(vcf_toks) != (num_samples + 9):
        raise ValueError("Something is rotten in the vcf line\n" + vcf_line)
    legend_file.write(" ".join([vcf_toks[x] for x in [2, 1, 3, 4]]) + "\n")
    for index, geno in enumerate(vcf_toks[9:]):
        haps[2*index] += geno[0]
        haps[2*index + 1] += geno[2]


def main():
    """Do all the work here."""
    args = parse_args()
    if args.inputFile[-3:] == ".gz":
        infile = gzip.open(args.inputFile)
    else:
        infile = open(args.inputFile)
    # Skip the entire header section
    for line in infile:
        toks = line.strip().split()
        if toks[0] == "#CHROM":
            num_samples = len(toks) - 9
            break
    haps = []
    for i in range(2*num_samples):
        haps.append("")
    # Open the output files
    legend_file = gzip.open(args.outPrefix + ".legend.gz", "wb")
    # Now process one vcf line at a time
    cnt = 0
    partnum = 0
    for line in infile:
        process_one_vcf_line(line, legend_file, haps, num_samples)
        cnt = cnt + 1
        if cnt % args.partLength == 0:
            haps_file = gzip.open(args.outPrefix + ".part" + str(partnum) +
                                  ".haps.gz", "wb")
            for hap in haps:
                haps_file.write(hap)
                haps_file.write("\n")
            haps_file.close()
            partnum = partnum + 1
            del haps[:]
            for i in range(2*num_samples):
                haps.append("")
    # check for leftovers
    if cnt % args.partLength != 0:
        haps_file = gzip.open(args.outPrefix + ".part" +
                              str(args.partLength) + ".haps.gz", "wb")
        for hap in haps:
            haps_file.write(hap)
            haps_file.write("\n")
        haps_file.close()
        del haps[:]
    legend_file.close()
    infile.close()


main()
