#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import sys
import logging

import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self, input_dim, num_classes, dropout = 0.2):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 512)
        self.activation1 = nn.ReLU() # 1
        self.dropout1 = nn.Dropout(dropout)
        self.fc2 = nn.Linear(512, 64)
        self.activation2 = nn.ReLU() # 2
        self.dropout2 = nn.Dropout(dropout)
        self.fc3 = nn.Linear(64, num_classes)

    def forward(self, x):
        x = self.activation1(self.fc1(x))
        x = self.dropout1(x)
        x = self.activation2(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        #x = F.softmax(self.fc3(x))
        return x

def parse_args():
    parser = argparse.ArgumentParser(
        description="Methylation-based squamous cell carcinoma classifier."
    )

    parser.add_argument(
        "-i", "--input",
        type=Path,
        help="Methylation tab-delimited file (beta values)."
    )

    parser.add_argument(
        "-s", "--probelist",
        type=Path,
        help="List of selected probes."
    )

    parser.add_argument(
        "-n", "--nnstate",
        type=Path,
        help="Saved state of neural network."
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output.tsv"),
        help="Path to output confidence values to (default: output.tsv)."
    )

    return parser.parse_args()

logging.basicConfig(
    filename='validation_errors.log',
    filemode='a',  # Append to existing log
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def validate_tsv(filepath, max_columns=10000):
    try:
        df = pd.read_csv(filepath, sep='\t', index_col=0)
    except Exception as e:
        raise ValueError(f"Error reading TSV: {e}")

    if not df.applymap(lambda x: isinstance(x, (int, float))).all().all():
        raise ValueError("File contains non-numeric values")
    if not ((df >= 0) & (df <= 1)).all().all():
        raise ValueError("Must supply beta values (between 0 and 1, inclusive)")
    if df.shape[1] > max_columns:
        raise ValueError(f"Number of columns exceeds {max_columns}")
    if not df.index.to_series().astype(str).str.startswith('cg').all():
        raise ValueError("Row names (probe names) should start with 'cg'")
    if df.columns.duplicated().any():
        # NOTE: will never reach here because of pandas automatic renaming
        raise ValueError("Column (sample) names are non-unique")

    logging.info(f"{filepath} passed all validation checks")
    return df

def validate_files(files):
    for file in files:
        if not file.exists():
            raise FileNotFoundError(f"File not found: {file}")
        if not file.is_file():
            raise ValueError(f"Not a valid file: {file}")

def process_files(files, output):
    # Example: concatenate contents
    with open(output, "w") as fout:
        for file in files:
            with open(file, "r") as fin:
                fout.write(fin.read())
                fout.write("\n")

def main():
    args = parse_args()
    CLASSES = ['BLCA', 'CESC', 'ESCA', 'HNSC', 'LUSC']
    num_classes = len(CLASSES)

    try:
        validate_files([args.input, args.probelist, args.nnstate])

        net = Net(10000, num_classes, dropout=0.5)
        net.load_state_dict(torch.load(args.nnstate, map_location=torch.device("cpu")))
        
        with open(args.probelist, 'r') as file:
            selected_probes = [line.strip() for line in file.readlines()]

        net = Net(10000, num_classes, dropout=0.5)
        net.load_state_dict(torch.load(args.nnstate, map_location=torch.device("cpu")))

        test_data = validate_tsv(args.input)
        
        missing_probes = [elem for elem in selected_probes if elem not in test_data.index]
        if missing_probes:
            raise ValueError(f"The following required probes are missing from the data: {missing_probes}")
        test_data = test_data.loc[selected_probes,:]
        
        input = torch.tensor(test_data.astype('float32').T.values)
        net.eval()
        with torch.inference_mode():
            # Should only be one iteration
            nn_output = F.softmax(net(input))
        
        output_confidence = pd.DataFrame(nn_output.to('cpu'), index=test_data.columns, columns = CLASSES)
        output_confidence.to_csv(args.output, sep='\t')
    except Exception as e:
        logging.error(f"Exception caught: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()