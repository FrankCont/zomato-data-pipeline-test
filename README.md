Data Pipeline Test

This repo contains a small pipeline that covers Module 1 and Module 2 from the coding test instructions.
It’s written in Python with pandas.

Layout


```text
project/
├── input_files/
├── output_files/
├── invalid_files/
├── processed_files.txt
├── main.py
├── file_checks.py
├── data_quality.py
└── README.md
```

What it does

Module 1 – File Check (file_checks.py)
basic_file_check() makes sure:
file hasn’t been processed before (processed_files.txt)
file isn’t empty
extension is .csv
If a file fails, it gets moved into invalid_files/.
save_as_done() records a file once processed.

Module 2 – Data Quality (data_quality.py)
quality_check() cleans and validates the data:
Cleans phone numbers (+, spaces removed). Splits into phone_1, phone_2.
Removes junk characters from address and reviews_list.
Required fields: name, phone_1, location. Rows missing them go into the .bad file.
Outputs:
.out  good rows
.bad  bad rows
.json  metadata (row numbers with issues)

How to run

Install pandas:
pip install pandas
Place csv files into input_files/.
Run the pipeline:
python main.py
Results show up in output_files/.
Bad/duplicate/empty files land in invalid_files/.

Example output

If you process data_file_20210527182730.csv, you will get:
data_file_20210527182730.out  clean records
data_file_20210527182730.bad  rows missing required fields
data_file_20210527182730.json  metadata like:
{
  "name_null": [2, 7],
  "location_null": [5]
}
