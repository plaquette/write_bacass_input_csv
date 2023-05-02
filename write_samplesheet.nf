#!/usr/bin/env nextflow
nextflow.enable.dsl=2


process write_samplesheet_p{
    
    label 'q_mini'

    input:
    tuple val(sampleName), path(inputFiles)


    output:
    tuple val(sampleName), path(inputFiles), path("*_samplesheet.csv"),  emit: tuple_with_samplesheet
    

    script:
    """

    python3 $baseDir/scr/write_samplesheet.py ${sampleName} ${inputFiles}

    """
}


// process check_fastq_files_p{
    
//     input:
//     tuple val(sampleName), path(inputFiles), path(csv)


//     output:
//     tuple env(is_valid), val(sampleName), path(inputFiles), path(csv),  emit: tuple_with_samplesheet_valid_key
    

//     script:
//     """

//     read is_valid <<< \$(python3 $baseDir/scr/check_fastq.py ${inputFiles})


//     """
// }


process check_fastq_files_with_skewer_p{
    
    label 'q_medium'

    input:
    tuple val(sampleName), path(inputFiles), path(csv)

    output:
    tuple env(is_valid), val(sampleName), path(inputFiles), path(csv),  emit: tuple_with_samplesheet_valid_key
    

    script:
    """

    touch status.txt

    pairno=0

    echo "${inputFiles}" | xargs -n2 | while read fq1 fq2; do
        skewer -m pe -q 3 -n --quiet -t 8 \$fq1 \$fq2 && echo "okay" > status.txt || echo "not_okay" > status.txt
    done

    is_valid=\$(cat status.txt)

    """
}


process publish_csv_p{

    label 'q_mini'

    publishDir params.out,
    mode : 'copy',
    pattern : "${params.run}/result.csv"
    
    input:
    path(csv)

    output:
    path("${params.run}/result.csv", emit: csv)
    
    script:
    """
    mkdir -p ${params.run}

    cp result.csv ${params.run}

    """
}




workflow write_it{

    take: data
    
    main:

        input_ch = Channel.fromPath(data.input + "/*.fastq.gz")

        in_grouped = input_ch.map{it -> [it.getName().split("\\.")[0].split("\\_")[0], it] }.groupTuple(by: 0)

        write_samplesheet_p(in_grouped)

        check_fastq_files_with_skewer_p(write_samplesheet_p.out)

        check_fastq_files_with_skewer_p.out.branch { it ->
                                                        valid: it[0]=="okay"
                                                        not_valid: it[0]=="not_okay"
                                                    }.set{skewer_out_sorted}

        csv_ch = skewer_out_sorted.valid.map{it -> it[3]}.collectFile(name:'result.csv', sort: true, newLine: false, keepHeader: true, skip: 1)

        publish_csv_p(csv_ch)


}

workflow{
    
    params.run = 'test'

    params.in = "$baseDir/in_example"

    params.out = "$baseDir/out/"


    data = [input: params.in, run: params.run, out: params.out]
    main:
        write_it(data)
        
}

