---
type: table
table_id: "04"
paper_key: "olmo2"
data_file: "olmo2-table-04.csv"
caption: "Table 3 OLMo 2 hyperparameters."
---

# Table 04

## Caption
Table 3 OLMo 2 hyperparameters.

## Data

|                         | OLMo27B        | OLMo213B       | OLMo232B       |
|-------------------------|----------------|----------------|----------------|
| Layers                  | 32             | 40             | 64             |
| Hidden Size ( d model ) | 4096           | 5120           | 5120           |
| Attention Heads(Q/KV)   | 32/32 (MHA)    | 40/40 (MHA)    | 40/8 (GQA)     |
| Batch Size              | 1024           | 2048           | 2048           |
| SequenceLength          | 4096           | 4096           | 4096           |
| Gradient Clipping       | 1.0            | 1.0            | 1.0            |
| Peak LR                 | 3 . 0 ⋅ 10 - 4 | 9 . 0 ⋅ 10 - 4 | 6 . 0 ⋅ 10 - 4 |
| LRWarmup                | 2000 steps     | 2000 steps     | 2000 steps     |
| LR Schedule (Cosine)    | 5T tokens      | 5T tokens      | 6.5T tokens    |
| LR Schedule Truncation  | (after 4T)     | n/a            | after 6T       |
