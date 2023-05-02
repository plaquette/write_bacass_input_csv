# write_samplesheet.nf


## Overview

This Nextflow workflow is designed to perform the following tasks:

1. Generate a samplesheet for each sample using the provided input files.
2. Check the quality of FastQ files using the Skewer tool.
3. Publish the final CSV file containing the results in the specified output directory.

To give you a samplesheet.csv from your *.fastq.gz files to be assembled with the nf-core/bacass pipeline [nf-core/bacass pipeline.](https://nf-co.re/bacass)


## Prerequisites

To run this workflow, you need to have the following installed:

- Nextflow (version 20.10.0 or higher)
- Python3 (for running the Python scripts)
- Skewer (for checking the FastQ files)

## Input

This workflow requires the input FastQ files to be placed in the specified input directory. The input files should have a `.fastq.gz` extension.

Overwrite the input directory using the `params.in` parameter in the workflow with:

`--in=.../path_to_your_data/...`


## Output

The output directory for the final CSV file can be overwritten using the `params.out` parameter in the workflow:

`--out=.../path_to_where_to_store_your_file`

The final CSV file will be named `result.csv` and stored in the specified output directory.

## Workflow Steps

The workflow consists of the following main steps:

1. `write_samplesheet_p`: Generates a samplesheet for each sample using the provided input files.
2. `check_fastq_files_with_skewer_p`: Checks the quality of FastQ files using the Skewer tool.
3. `publish_csv_p`: Publishes the final CSV file containing the results in the specified output directory.

## Execution

To run the workflow, navigate to the directory containing the Nextflow script and execute the following command:

`nextflow run write_samplesheet.nf`

or to run it on a slurm cluster

`nextflow run write_samplesheet.nf -profile cluster`


This will start the workflow using the default input and output directories.

## Customization

This workflow can be customized by modifying the `params` values or by adding additional processes or steps to the existing workflow.

## Disclaimer
The `write_samplesheet_p`-process is as unefficent as it gets.
