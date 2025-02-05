# scopus-llm-review

## Overview
This repository contains an experiment using the Gemma2 language model to evaluate the relevance and usefulness of article abstracts retrieved from Scopus. The study runs a Scopus query, processes the results, and applies an LLM-based review to assess their pertinence.

## Files
- **20241121-scopus.csv** – Raw Scopus export of article abstracts and metadata.
- **20241121-scopus-gemma-2-27b-it-Q6_K_L.csv** – Processed results including LLM-based relevance assessments.
- **LICENSE** – Repository licensing information.
- **README.md** – This file.
- **scopus_query.sql** – SQL query used to retrieve abstracts from Scopus.
- **scopus_review.py** – Script for running the LLM evaluation on the Scopus data.

## Usage
1. **Retrieve Data** – Run `scopus_query.sql` in Scopus to obtain a list of relevant abstracts.
2. **Run Evaluation** – Use `scopus_review.py` to process `20241121-scopus.csv` and generate LLM-based assessments.
3. **Review Output** – Results are stored in `20241121-scopus-gemma-2-27b-it-Q6_K_L.csv` for further analysis.

## Requirements
- Python 3.x
- Required dependencies (install via `pip install -r requirements.txt`)
- Access to Scopus for querying articles
- Gemma2 model (downloadable from [Huggingface](https://huggingface.co/bartowski/gemma-2-27b-it-GGUF)) or an alternative LLM for use in LlamaCPP

## License
This project is licensed under the terms specified in the `LICENSE` file.

## Contact
For questions or contributions, please open an issue or submit a pull request.

