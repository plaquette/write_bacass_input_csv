import click
import pandas as pd
import os



@click.command()
@click.argument("src", nargs=-1)
def write_samplesheet(src):

    sample_name = src[0]

    fastq = []

    for f in sorted(list(src[1:])):
        fastq.append(os.path.abspath(f))



    d = {'ID': sample_name, 'R1': fastq[0], 'R2': "NA", 'LongFastQ': "NA", 'Fast5': "NA", 'GenomeSize': "NA"}

    if len(fastq) == 2:
        d['R2'] = fastq[1]

    df = pd.DataFrame(d, index=[0])

    df.set_index('ID', inplace=True)


    dir_path = os.path.dirname(fastq[0])


    samplesheet_path = f"{dir_path}/{sample_name}_samplesheet.csv"


    df.to_csv(samplesheet_path, sep='\t', index=True)





write_samplesheet()