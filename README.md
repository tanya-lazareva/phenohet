# Statistical dissection of the genetic determinants of phenotype heterogeneity in genes with multiple associated rare diseases
The purpose of this project is to systematically analyse the potential gene-level factors (the number of non-functional alleles, localization of the variant in the coding part of the gene and  variant type) that may be causal for differences in the phenotype presentation of diseases associated with a single gene. 
## Prerequisites
- [Python](https://www.python.org/downloads/) version 3.8 or higher
- [R](https://cran.r-project.org/mirrors.html) version 3.6 or higher
- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Jupyter Notebook](https://anaconda.org/anaconda/jupyter)
- [BCFtools](https://anaconda.org/bioconda/bcftools)
- [GATK](https://anaconda.org/bioconda/gatk)
## Installation
### Python

You can install the required dependencies by running the following command in the terminal from the project root directory:

```shell
pip3 install -r requirements.txt
```

### R
You can install the required dependencies by running the following command in the terminal from the project root directory:
```
Rscript requirements.R
```
## Description
To anlyse the impact of genetic factors on heterogenous gene-disease relationship the data from [NCBI ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) and [Human Phenotype Ontology (HPO)](HPO.jax.org/) was collected. 

The [DataParser.ipynb](https://github.com/tanya-lazareva/phenohet/blob/main/DataParser.ipynb) script gathers pathogenic and likely pathogenic genetic variants for OMIM diseases from NCBI ClinVar, as well as associations between genes and monogenic disorders from  Human Phenotype Ontology (HPO) Annotations. All the collected data is then merged for further analysis.

In the next step, the [GenesMultipleDiseases.ipynb](https://github.com/tanya-lazareva/phenohet/blob/main/GenesMultipleDiseases.ipynb) script characterizes genes that are associated with two or more monogenic diseases using contraint metrics, GTEx data,HPO terms and enrichment in biological pathways.

[Genes2Diseases.ipynb](https://github.com/tanya-lazareva/phenohet/blob/main/Genes2Diseases.ipynb) -  statistical analysis of the impact of causal variant localization and variant type on the determination of phenotype associated with genes linked to exactly two monogenic disorders.

## Citing



