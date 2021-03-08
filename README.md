# coverage_test
Task to create an NGS coverage report that highlights genes with sub-optimal coverage.

## Installation

Example setup for the system and the repository is show below using python's virtual environment. 

### Systmem requirements

At least python3.6 is required for this project.

### Virtual environment setup

1. Clone repository
    ```
    git clone https://github.com/mlgosh/coverage_test.git
    ```
2. With python3.6, set up virtual environment. Example below:
    ```
    cd test_coverage
    # Create the virtual environment
    python3.6 -m venv .venv
    # Enable the virtual environment
    source .venv/bin/activate
    ```
3. Install requirements
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Move to scripts directory
    ```
    cd scripts
    ```
3. Run coverage.py. You must provide the path to a sambamba_ouput.txt file that you wish to analyse. It can be provided as an argument using an -i or --input tag. 
    ```
    python3.6 coverage.py -i ../test_data/NGS148_34_139558_CB_CMCMD_S33_R1_001.sambamba_output.txt
    ```
5. A coverage report, in csv format, is generated and can be found in the results directory. The report lists the genes with sub-optimal coverage alongside the percentage 30x for the gene.

## Testing

A number of unit tests have been written to test the main functions of the coverage.py script. 

1. To run this, first change line 5 of the test_coverage.py script to contain the path to the scripts directory on your machine.
    ```
    sys.path.append("<path on your machine>/coverage_test/scripts")
    ```
2. Then run the script like so. This can be run from any directory.
    ```
    pytest tests/test_coverage.py
    ```

## Future development

Currently the script requires a sambamba_output.txt file to be given as an argument when running the script. In future it could be desirable to search a given folder(s) for these files so that many can be processed at once.
