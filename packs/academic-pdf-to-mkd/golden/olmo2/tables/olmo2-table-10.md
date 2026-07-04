---
type: table
table_id: "10"
paper_key: "olmo2"
data_file: "olmo2-table-10.csv"
caption: "Table 8 Results on 9 multiple-choice tasks from the validation subset of OLMES ( cloze formulation format) for various peak learning rates and schedule lengths. Average scores vary by less than two points across all variants, with most scores within half a point of each other."
---

# Table 10

## Caption
Table 8 Results on 9 multiple-choice tasks from the validation subset of OLMES ( cloze formulation format) for various peak learning rates and schedule lengths. Average scores vary by less than two points across all variants, with most scores within half a point of each other.

## Data

| Learning Rate   | Pretraining Stage   | Mid-training Stage       |   OLMES (CF, valid) |
|-----------------|---------------------|--------------------------|---------------------|
| 3 ⋅ 10 - 4      | 300B tokens         | 50B tokens               |                62.5 |
| 6 ⋅ 10 - 4      | 300B tokens         | 50B tokens               |                63.9 |
| 9 ⋅ 10 - 4      | 300B tokens         | 50B tokens               |                64.1 |
| 12 ⋅ 10 - 4     | 300B tokens         | 50B tokens               |                63.6 |
| 6 ⋅ 10 - 4      | 300B tokens         | 100B tokens              |                64.6 |
| 9 ⋅ 10 - 4      | 300B tokens         | 100B tokens              |                64.5 |
| 12 ⋅ 10 - 4     | 300B tokens         | 100B tokens              |                64.2 |
| 3 ⋅ 10 - 4      | 2T tokens           | 100B high quality tokens |                73.8 |
| 6 ⋅ 10 - 4      | 2T tokens           | 100B high quality tokens |                73.9 |
