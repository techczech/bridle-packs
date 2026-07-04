---
type: table
table_id: "16"
paper_key: "olmo2"
data_file: "olmo2-table-16.csv"
caption: "Table 14 Comparison of six mid-training mixes between best single checkpoint and the average of three checkpoints ( soup ) trained on different data permutations. We run all experiments starting from 7B pretrained checkpoint; we run mid-training stage for 50B tokens. Souping consistently equals or outperform the single best checkpoint trained on the same mix."
---

# Table 16

## Caption
Table 14 Comparison of six mid-training mixes between best single checkpoint and the average of three checkpoints ( soup ) trained on different data permutations. We run all experiments starting from 7B pretrained checkpoint; we run mid-training stage for 50B tokens. Souping consistently equals or outperform the single best checkpoint trained on the same mix.

## Data

| Mid-training mix   | Mid-training mix   |   OLMES (MCF) |   OLMES-Gen |   MMLU (MCF) |   GSM* |
|--------------------|--------------------|---------------|-------------|--------------|--------|
| A                  | best single        |          75.6 |        68.5 |         61.2 |   71   |
| A                  | 3 x soup           |          77   |        69.4 |         62   |   74   |
| B                  | best single        |          75.3 |        69.9 |         61.5 |   73   |
| B                  | 3 x soup           |          77.3 |        70.1 |         62.7 |   77   |
| C                  | best single        |          76.3 |        70.9 |         62.8 |   66   |
| C                  | 3 x soup           |          76.8 |        71.3 |         63.5 |   66   |
| D                  | best single        |          77.5 |        71.2 |         63.4 |   59.5 |
| D                  | 3 x soup           |          77.8 |        71.7 |         63.5 |   60   |
| E                  | best single        |          73.4 |        63.1 |         62.2 |   60.5 |
| E                  | 3 x soup           |          75.3 |        64.2 |         63.1 |   43   |
| F                  | best single        |          77.1 |        69.9 |         63.7 |   73.5 |
| F                  | 3 x soup           |          77.9 |        70.4 |         63.7 |   74.5 |
