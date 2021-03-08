import argparse 
import csv
from statistics import mean

class Coverage():

    def __init__(self, input_file):
        self.file_path = input_file
        self.file_name = input_file.split('/')[-1]
        # Error raised if the input file is not a sambamba output file
        if not self.file_name.endswith('sambamba_output.txt'):
            raise ValueError("This file type is not supported")

    def parse_sambamba_output(self):
        """
        This function parses the sambamba output file and returns a list of dictionaries.
        Each dictionary contains the information for one exon.
        """
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
        """
        This function takes the exons list as an input.
        Returns a dictionary of dictionaries.
        
        Loops through the list of exons, adds genes to a dictionary, if not already present.
        Each gene is the key for a dictionary which contains a list of the percentage30 for each exon.
        If any exon has failed the coverage threshold the gene is marked as having failed.
        """
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
        """
        This function takes the genes dictionary as an input.
        Returns a list of failed genes, each failed gene is a dictionary.

        Identifies genes which have been flagged with a coverage failure.
        Takes a mean of the exons coverage for the gene. Stores in a dictionary.
        """
        failed_genes = []
        for gene in genes:
            if genes[gene]['failed'] == 'Y':
                failed_genes.append({'GeneSymbol;Accession': gene, 'percentage30': mean(genes[gene]['percentage30'])})
        return failed_genes

    def write_output(self, failed_genes):
        """
        This function takes the list of failed genes as an input.
        Creates a csv file with the genes that failed the coverage threshold and the total percentage30 for the gene.
        """
        file_prefix = self.file_name.strip('sambamba_output.txt')
        fieldnames = ['GeneSymbol;Accession', 'percentage30']
        with open (f'../results/{file_prefix}.coverage_output.csv', 'w', newline = '') as output:
            csvwriter = csv.DictWriter(output, fieldnames=fieldnames)
            csvwriter.writeheader()
            csvwriter.writerows(failed_genes)

    def main(self):
        exons = self.parse_sambamba_output()
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