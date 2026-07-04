---
type: table
table_id: "13"
paper_key: "olmo2"
data_file: "olmo2-table-13.csv"
caption: "Table 11 Comparison of mid-training mixes introduced in Table 10. Each row corresponds to a 50 billion token training run following learning rate schedule described in Section §4.1 (except first row). Weights are initialized from a OLMo 2 checkpoint pretrained for 4T tokens. We compare each run on a mix of OLMES core tasks (multiple choice format; see Table 6), OLMES generative tasks (Table 6), MMLU (multiple choice format; Hendrycks et al., 2021a), and a random sample of 200 GSM8K (Cobbe et al., 2021) questions we use as development set (GSM*; Section §A.1). Results on the final mid-training mix are in Table 9."
---

# Table 13

## Caption
Table 11 Comparison of mid-training mixes introduced in Table 10. Each row corresponds to a 50 billion token training run following learning rate schedule described in Section §4.1 (except first row). Weights are initialized from a OLMo 2 checkpoint pretrained for 4T tokens. We compare each run on a mix of OLMES core tasks (multiple choice format; see Table 6), OLMES generative tasks (Table 6), MMLU (multiple choice format; Hendrycks et al., 2021a), and a random sample of 200 GSM8K (Cobbe et al., 2021) questions we use as development set (GSM*; Section §A.1). Results on the final mid-training mix are in Table 9.

## Data

| Mid-training mix           |   OLMES (MCF) |   OLMES-Gen |   MMLU (MCF) |   GSM* |
|----------------------------|---------------|-------------|--------------|--------|
| n/a (pretrain checkpoint)  |          69.6 |        63.2 |         59.8 |   28.5 |
| PT Mix                     |          74   |        64.5 |         61.8 |   27   |
| Web FT 7                   |          73.5 |        64.1 |         61.9 |   24.5 |
| Web FT 7 FW 3              |          73.5 |        63   |         62.4 |   30.5 |
| Web FT 7 FW 2              |          75.2 |        63.8 |         63.1 |   28.5 |
| Web FT 7 FW 2 + Ins        |          74.2 |        64.1 |         63   |   46   |
| Web FT 7 FW 2 + Math       |          75.7 |        69.7 |         62.3 |   52   |
| Web FT 7 FW 2 + Math + Ins |          75.7 |        70.2 |         63.1 |   46.5 |
