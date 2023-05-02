import click
import os
import gzip
from Bio import SeqIO


def is_fastq(filename):
    """Check if a file is in the Fastq format."""
    try:
        with open_file(filename) as f:
            for record in SeqIO.parse(f, "fastq"):
                pass
    except (ValueError, TypeError, FileNotFoundError):
        return False
    return True

# def is_fastq(filename):
#     """Check if a file is in the Fastq format."""
#     # Check if file is empty
#     if os.path.getsize(filename) == 0:
#         return False

#     with open_file(filename) as f:
#         line_num = 0
#         for line in f:
#             line_num += 1
#             if line_num == 1:
#                 if not line.startswith('@'):
#                     return False
#             elif line_num == 2:
#                 if not all(c in 'ACGTN' for c in line.strip()):
#                     return False
#                 quality_scores_len = len(line.strip())
#             elif line_num == 3:
#                 if not line.startswith('+'):
#                     return False
#             elif line_num == 4:
#                 if len(line.strip()) != quality_scores_len:
#                     return False
#                 break
#     return True


def get_quality_encoding(filename):
    """Get the quality score encoding of a Fastq file."""
    quality_scores = ''
    with open_file(filename) as f:
        for line_num, line in enumerate(f):
            if line_num == 3:
                quality_scores = line.strip()
                break
    if quality_scores == '':
        return 'Unknown'
    ascii_values = [ord(c) for c in quality_scores]
    if max(ascii_values) <= 74:
        return 'Sanger'
    elif min(ascii_values) >= 64:
        return 'Illumina 1.8+'
    else:
        return 'Unknown'


def open_file(filename):
    """Open a Fastq file, handling compressed and uncompressed files."""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename)



@click.command()
@click.argument("src", nargs=-1)
def check_fastq(src):

    filenames = []

    for f in sorted(list(src[0:])):
        filenames.append(os.path.abspath(f))

    if len(filenames) == 1:
        filename1 = filenames[0]
        if is_fastq(filename1):
            print('okay')
        else:
            print('not_okay')
    elif len(filenames) == 2:
        filename1, filename2 = filenames
        if is_fastq(filename1) and is_fastq(filename2):
            encoding1 = get_quality_encoding(filename1)
            encoding2 = get_quality_encoding(filename2)
            if encoding1 == encoding2:
                print('okay')
            else:
                print('not_okay')
        else:
            print('not_okay')
    else:
        print('not_okay')


check_fastq()