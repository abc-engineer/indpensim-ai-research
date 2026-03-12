# IndPenSim AI Research
> AI-based research in Biopharmaceutical Batch Processes using the **IndPenSim (Industrial Penicillin Simulation)** Dataset.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/framework-PyTorch%20/%20TensorFlow-orange.svg)


## Repository Structure

```
├── configs/            # Experiment configuration files
│   ├── environment.yml
│   ├── pca_config.yaml
│   ├── lstm_ae_config.yaml
│   └── training_config.yaml
│
├── data/               # Raw and processed IndPenSim data
│   ├── raw/            # Original dataset (read-only, do not modify)
│   └── processed/      # Preprocessed data generated from the raw dataset
│
├── notebooks/          # Exploratory analysis and experimental prototypes
│
├── src/                # Core source code
│   ├── preprocessing.py
│   ├── models.py       # Deep learning model architectures
│   └── trainer.py      # Training and evaluation pipeline
│
├── experiments/        # Experiment configurations and experiment-specific artifacts
│   ├── exp01_pca
│   └── exp02_fault_detection
│
├── results/            # Saved models and visualization outputs
│   ├── figures
│   ├── tables
│   ├── models
│   └── logs
│
├── README.md
└── .gitignore
```

---

## Dataset: IndPenSim

The **IndPenSim (Industrial Penicillin Simulation)** dataset simulates a **100,000 L industrial fed-batch penicillin fermentation process**.

Key characteristics:

* **Multivariate Process Data**
  More than 70 process variables including:

  * pH
  * Dissolved Oxygen (DO)
  * Temperature
  * Feed rate
  * Raman spectroscopy signals

* **Fault Scenarios**
  The dataset includes simulated industrial fault conditions such as:

  * Sensor failures
  * Feed disturbances
  * Process deviations

This dataset is widely used as a **benchmark for bioprocess monitoring and fault detection research**.  

Download: [IndPenSim Dataset(link)](http://www.industrialpenicillinsimulation.com/index.html)  

---

## Technology Stack

**Language**
* Python 3.x

**Deep Learning**
* PyTorch / TensorFlow

**Data Analysis**
* Pandas
* NumPy
* Scikit-learn

**Visualization**
* Matplotlib
* Seaborn

---


## Author

Name:  
Affiliation:  
Contact:  
