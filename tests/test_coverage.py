import pytest
import sys
import warnings

sys.path.append("/home/maria/cambridge/coverage_test/scripts")

from coverage import Coverage

class TestReadSambambaOutput():
    
    def setup(self):
        self.file_path = '/home/maria/cambridge/coverage_test/test_data/test.sambamba_output.txt'
        self.parser = Coverage(self.file_path)
        self.expected_output = [{'#chromosome': '1', 'StartPosition': '26126711', 
                                'EndPosition': '26126914', 'FullPosition': '1-26126711-26126914', 
                                'NotUsed': '+', 'GeneSymbol;Accession': 'SELENON;NM_020451.2', 
                                'Size': '57190', 'readCount': '142', 'meanCoverage': '39.5222', 
                                'percentage30': '49.2611', 'sampleName': '1'}, 
                                {'#chromosome': '1', 'StartPosition': '26127523', 
                                'EndPosition': '26127661', 'FullPosition': '1-26127523-26127661', 
                                'NotUsed': '+', 'GeneSymbol;Accession': 'SELENON;NM_020451.2', 
                                'Size': '57190', 'readCount': '5748', 'meanCoverage': '3501.21', 
                                'percentage30': '100', 'sampleName': '1'}]

    def test_read_sambamba_output(self):
        output = self.parser.read_sambamba_output()
        assert output == self.expected_output

class TestAlmalgamatGenes():
    
    def setup(self):
        self.parser = Coverage('input_file.sambamba_output.txt')

    @pytest.mark.parametrize("exons, expected_output", [
       ([{'GeneSymbol;Accession': 'SELENON;NM_020451.2', 'percentage30': '49.2611'}, 
       {'GeneSymbol;Accession': 'SELENON;NM_020451.2','percentage30': '100'}], 
       {'SELENON;NM_020451.2': {'percentage30': [49.2611, 100.0], 'failed': 'Y'}}), 
       ([{'GeneSymbol;Accession': 'POMGNT1;NM_001243766.1', 'percentage30': '100'}, 
       {'GeneSymbol;Accession': 'POMGNT1;NM_001243766.1','percentage30': '100'}], 
       {'POMGNT1;NM_001243766.1': {'percentage30': [100.0, 100.0], 'failed': 'N'}}),   
       ([{'GeneSymbol;Accession': 'SELENON;NM_020451.2', 'percentage30': '100'}, 
       {'GeneSymbol;Accession': 'POMGNT1;NM_001243766.1','percentage30': '100'}], 
       {'SELENON;NM_020451.2': {'percentage30': [100.0], 'failed': 'N'},
       'POMGNT1;NM_001243766.1': {'percentage30': [100.0], 'failed': 'N'}})
    ])

    def test_amalgamate_genes(self, exons, expected_output):
        output = self.parser.almalgamat_genes(exons)
        assert output == expected_output 

class TestIdentifyFailedGenes():

    def setup(self):
        self.parser = Coverage('input_file.sambamba_output.txt')

    @pytest.mark.parametrize("genes, expected_output", [
        ({'SELENON;NM_020451.2': {'percentage30': [100.0], 'failed': 'N'},
       'POMGNT1;NM_001243766.1': {'percentage30': [100.0], 'failed': 'N'}}, []),
        ({'SELENON;NM_020451.2': {'percentage30': [49.2611, 100.0], 'failed': 'Y'},
       'POMGNT1;NM_001243766.1': {'percentage30': [100.0], 'failed': 'N'}}, 
       [{'GeneSymbol;Accession': 'SELENON;NM_020451.2', 'percentage30': 74.63055}])
    ])

    def test_identify_failed_genes(self, genes, expected_output):
        output = self.parser.identify_failed_genes(genes)
        assert output == expected_output