# Client File Router
A Python script that automates sorting and transferring mortgage adviser client files into categorized folders (e.g. New Purchase, Refinance, Top-up).

This tool is designed to reduce manual file sorting for administrative workflows.

## Features 
- Detects, categorizes, and transfers recognized client files from download folder to matched directory 
- Transfer unrecognized client files to a new folder in given category
- Merge related client files into one folder
- Separate client files from an existing folder to new folder
- Transfer existing client folder
- Rename existing client folder
- Reset dummy client files to downloads folder (for testing)

## Prerequisites
- Install Python 3.14+: [Download Python](https://www.python.org/downloads/)

## Installation
1. Clone the repo:
```bash
git clone https://github.com/anaGianno/client-file-router.git
```

2. Navigate into the project:
```bash
cd client-file-router
```

## Usage
Run the program:
```bash
python main.py
```