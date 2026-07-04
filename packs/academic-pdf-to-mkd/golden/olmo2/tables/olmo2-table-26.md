---
type: table
table_id: "26"
paper_key: "olmo2"
data_file: "olmo2-table-26.csv"
caption: "Figure 22 The top row shows the training curves of OLMo-2-1124-13B-Instruct-Preview on verifiable rewards, KL divergence, and response lengths. In the bottom row, the y-axes show the average scores across our evaluation suites and GSM8K, IFEval, and MATH Flex scores, respectively. Overall, we found RLVR increases not only the training rewards of our 13B models but also the downstream evaluations such as GSM8K."
---

# Table 26

## Caption
Figure 22 The top row shows the training curves of OLMo-2-1124-13B-Instruct-Preview on verifiable rewards, KL divergence, and response lengths. In the bottom row, the y-axes show the average scores across our evaluation suites and GSM8K, IFEval, and MATH Flex scores, respectively. Overall, we found RLVR increases not only the training rewards of our 13B models but also the downstream evaluations such as GSM8K.

## Data

| Model                  |   Average |   AGI Eval English |   DeepMind Math |   GPQA |   IFEval OOD |   MMLU Pro |
|------------------------|-----------|--------------------|-----------------|--------|--------------|------------|
| OLMo 2 32B Instruct    |      44.9 |               68.3 |            34.7 |   35.9 |         33.1 |       52.7 |
| OLMo 2 32B DPO         |      43.8 |               68.6 |            34.5 |   35.7 |         26.8 |       53.3 |
| OLMo 2 32B SFT         |      39.3 |               63.9 |            33.4 |   32.6 |         20.4 |       46.3 |
| OLMo 2 1124 13B Inst.  |      35.2 |               60.5 |            26.8 |   28.8 |         18.7 |       41.4 |
| OLMo 2 1124 13B DPO    |      35.5 |               60.1 |            25.4 |   32.1 |         18   |       41.8 |
| OLMo 2 1124 13B SFT    |      33   |               56   |            27.1 |   27   |         16.6 |       38.2 |
| OLMo 2 1124 7B Inst.   |      32.2 |               57.2 |            19.1 |   30.1 |         18.7 |       36   |
| OLMo 2 1124 7B DPO     |      31.8 |               56.7 |            17.7 |   30.6 |         17.3 |       36.6 |
| OLMo 2 1124 7B SFT     |      29.8 |               52.7 |            19   |   27.7 |         16.2 |       33.2 |
| OLMo 7B 0724 Inst.     |      22.9 |               43.6 |             5.8 |   27.9 |         14.4 |       22.9 |
| OLMoE 1B 7B 0924 Inst. |      20.5 |               39.1 |             4.2 |   27.5 |         11.3 |       20.6 |
