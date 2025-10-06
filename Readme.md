Multi-Agent Cost-Aware Phishing Defense
This repository contains a multi-agent system designed to analyze and defend against phishing attacks. The system leverages HTML content crawling, feature extraction, and dataset analysis to identify and mitigate phishing threats.

Table of Contents
Overview
Features
Usage
Folder Structure
Contributing
License
Overview
Phishing attacks are a significant cybersecurity threat. This project implements a multi-agent system to analyze HTML content, extract features, and identify phishing URLs. The system is designed to be cost-aware, balancing computational efficiency with detection accuracy.

Features
HTML Content Crawling: Extracts and processes HTML content from URLs.
Feature Extraction: Analyzes HTML features to identify phishing indicators.
Batch Processing: Combines and processes multiple datasets for scalability.
Dataset Support: Includes the PhiUSIIL Phishing URL Dataset for analysis.

Usage
1. HTML Content Crawling
Run the dom_content_crawler_main.py script to crawl and extract HTML content:


python dom_content_crawler_main.py
2. Batch Combination
Combine multiple CSV files into a single dataset using batch_combiner.py:


python batch_combiner.py
3. Analyze HTML Features
Use the html_content_crawler.py script to analyze and extract features:


python html_content_crawler.py
Folder Structure
csvs: Contains CSV files with extracted HTML features and datasets.
html_features_all.csv: Combined dataset of all features.
html_features_batch_*.csv: Batch-wise feature datasets.
PhiUSIIL_Phishing_URL_Dataset.csv: Phishing URL dataset.
__pycache__: Compiled Python files for faster execution.
dom_content_crawler_main.py: Main script for HTML content crawling.
dom_content_crawler_script.py: Helper script for DOM content crawling.
html_content_crawler.py: Script for analyzing HTML features.
batch_combiner.py: Script for combining batch CSV files.
Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.