import argparse 
import csv
from statistics import mean

class Coverage():

    def __init__(self, input_file):
        self.file_path = input_file
        self.file_name = input_file.split('/')[-1]
        if not self.file_name.endswith('sambamba_output.txt'):
            raise ValueError("This file type is not supported")

    def read_sambamba_ouput(self):
        exons = []
        with open (self.file_path, "r") as sambamba_output:
            for line in sambamba_output:
                if line.startswith('#'):
                    fields = line.strip().split()
                else:
                    description = list(line.strip().split())
                    i = 0
                    exon_dict = {}
                    while i<len(fields):
                        exon_dict[fields[i]] = description[i]
                        i += 1
                    exons.append(exon_dict)
        return exons

    def almalgamat_genes(self, exons):
        genes = {}
        for exon in exons:
            gene = exon['GeneSymbol;Accession']
            percentage30 = float(exon['percentage30'])
            if gene not in genes:
                genes[gene] = {'percentage30': [percentage30], 'failed': 'N'}
            else:
                genes[gene]['percentage30'].append(percentage30)
            if percentage30 != 100:
                genes[exon['GeneSymbol;Accession']]['failed'] = 'Y'
        return genes

    def identify_failed_genes(self, genes):
        failed_genes = []
        for gene in genes:
            if genes[gene]['failed'] == 'Y':
                failed_genes.append({'GeneSymbol;Accession': gene, 'percentage30': mean(genes[gene]['percentage30'])})
        return failed_genes

    def write_output(self, failed_genes):
        fieldnames = ['GeneSymbol;Accession', 'percentage30']
        with open ('test.csv', 'w', newline = '') as output:
            csvwriter = csv.DictWriter(output, fieldnames=fieldnames)
            csvwriter.writeheader()
            csvwriter.writerows(failed_genes)

    def main(self):
        exons = self.read_sambamba_ouput()
        genes = self.almalgamat_genes(exons)
        failed_genes = self.identify_failed_genes(genes)
        self.write_output(failed_genes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='input file', required=True) # Want to add functionality to search for files
    args = vars(parser.parse_args())
    input_file = args['input']
    coverage_runner = Coverage(input_file)
    coverage_runner.main()
    print('Coverage.py completed successfully')