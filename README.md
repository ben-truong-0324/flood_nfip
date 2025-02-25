# Flood NFIP Insurance Prediction Project

This project leverages machine learning models to predict flood risk and insurance premiums based on the National Flood Insurance Program (NFIP) data. We explore a variety of techniques, including decision trees, bagging, and boosting, to predict the flood risk and associated insurance premiums for properties based on historical and geographical data.

## Project Overview

Data is retrieved from [NFIP Data Source](https://www.fema.gov/openfema-data-page/fima-nfip-redacted-claims-v2).  
In this project, we aim to predict flood risk and the corresponding insurance premiums using the provided NFIP dataset. This dataset includes multiple features such as property characteristics, flood zone designations, historical flood events, and policy information. Our goal is to develop models that can predict flood risk and premiums accurately using various regression and classification techniques.


## Installation and Setup
Setup your local MYSQL configs in .env_sample and rename it to .env

### **Setting up the Conda Environment**

To set up the project, it is recommended to use the provided `environment.yml` file to create a conda environment with the necessary dependencies.

```bash
conda env create -f environment.yml
conda env update --file environment.yml --prune
conda activate ml_general
python -m flood_nfip.ml

# download/copy data into ./data/
```

## License

Copyright (c) 2025 Ben Truong

Code and documentation copyright 2025 the author. Code released under the [MIT license](LICENSE).