---
type: table
table_id: "17"
paper_key: "olmo2"
data_file: "olmo2-table-17.csv"
caption: "Table 15 The OLMo 2 Instruct Evaluation Regime (Adapted from Lambert et al. (2024)): settings for development ( top ) and unseen ( bottom ) portions of the evaluation suite. CoT are evaluations run with chain of thought prompting (Wei et al., 2022). # shots is the number of in-context examples in the evaluation template. Chat indicates whether we use a chat template while prompting the model. Multiturn ICL indicates that we present each in-context example as a separate turn in a conversation (applicable only when a chat template is used and # Shots is not 0). ∗ Average over multiple sub-evaluations-full details of the safety evaluation are in Lambert et al. (2024)."
---

# Table 17

## Caption
Table 15 The OLMo 2 Instruct Evaluation Regime (Adapted from Lambert et al. (2024)): settings for development ( top ) and unseen ( bottom ) portions of the evaluation suite. CoT are evaluations run with chain of thought prompting (Wei et al., 2022). # shots is the number of in-context examples in the evaluation template. Chat indicates whether we use a chat template while prompting the model. Multiturn ICL indicates that we present each in-context example as a separate turn in a conversation (applicable only when a chat template is used and # Shots is not 0). ∗ Average over multiple sub-evaluations-full details of the safety evaluation are in Lambert et al. (2024).

## Data

| Category              | Benchmark     | CoT   |   #Shots | Chat   | Multiturn ICL   | Metric                 |
|-----------------------|---------------|-------|----------|--------|-----------------|------------------------|
| Knowledge Recall      | MMLU          | ✓     |        0 | ✓      | ✗               | EM                     |
| Knowledge Recall      | PopQA         | ✗     |       15 | ✓      | ✓               | EM                     |
| Knowledge Recall      | TruthfulQA    | ✗     |        6 | ✓      | ✗               | MC2                    |
| Reasoning             | BigBenchHard  | ✓     |        3 | ✓      | ✓               | EM                     |
| Reasoning             | DROP          | ✗     |        3 | ✗      | N/A             | F1                     |
| Math                  | GSM8K         | ✓     |        8 | ✓      | ✓               | EM                     |
| Math                  | MATH          | ✓     |        4 | ✓      | ✓               | Flex EM                |
| Instruction Following | IFEval        | ✗     |        0 | ✓      | N/A             | Pass@1 (prompt; loose) |
| Instruction Following | AlpacaEval 2  | ✗     |        0 | ✓      | N/A             | LC Winrate             |
| Safety                | Tülu 3 Safety | ✗     |        0 | ✓      | N/A             | Average ∗              |
