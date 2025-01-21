# CBB Paper: Harnessing CO2 Fixation and Reducing Power Recycling for Enhanced PHA Industrial Bioproduction

This repository contains the code and data supporting the paper titled **"Harnessing CO2 Fixation and Reducing Power Recycling for Enhanced PHA Industrial Bioproduction"**. The study investigates the impact of the Calvin-Benson-Bassham (CBB) cycle on biomass and polyhydroxyalkanoates (PHA) production.

## Folder Structure

The repository is organized into the following main folders:

### 1. **FBA Folder**  
Contains metabolic models used to evaluate the impact of the CBB cycle on biomass production via **Flux Balance Analysis (FBA)**. This folder includes:
- Metabolic models for H16 strains using paml oil as carbon source.
- Scripts and analysis to assess biomass yield under different conditions with CBB cycle incorporation.

### 2. **RBA Folder**  
Contains **Resource Balance Analysis (RBA)** metabolic models and related scripts to assess the impact of the CBB cycle on biomass production. This includes:
- Metabolic models for H16 strains using paml oil as carbon source and enzymy kapp were evalued with protome.
- Scripts and analysis to assess biomass yield under different conditions with CBB cycle incorporation.

### 3. **RNAseq Folder**  
Contains the transcriptomic expression profiles used in this paper, including gene expression data for:
- **H16G** (wild-type strain)
- **cbb1-7** (CBB-engineered strains)
### Prerequisites
Ensure you have the following installed to run the models and scripts:
- Python (for scripts in the **FBA** and **RBA** folders)
- R (for running any R-based scripts or visualizations)
- Additional dependencies as specified in the respective script headers.
## Citation
If you use this repository for your work, please cite the paper:

- **Harnessing CO2 Fixation and Reducing Power Recycling for Enhanced PHA Industrial Bioproduction**

## License
This repository is licensed under the MIT License.
