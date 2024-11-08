Create a CLI tool which:
* Takes in a CSV file containing the following columns:
* `firstname`: String
* `lastname`: String
* `date`: String (format YYYY-MM-DD)
* `division`: Integer
* `points`: Integer
* `summary`: String
* Sorts the records by `division` and `points`.
* Selects the top three records.
* Prints the records to stdout in the following YAML format:
records:
- name:
details: In division from performing
- name:
details: In division from performing
- name:
details: In division from performing
