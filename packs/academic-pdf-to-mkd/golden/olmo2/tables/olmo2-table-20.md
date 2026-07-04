---
type: table
table_id: "20"
paper_key: "olmo2"
data_file: "olmo2-table-20.csv"
caption: "Finally, we evaluate OLMo 2-Instruct on the unseen evaluation suite from Lambert et al. (2024) without the code evaluation tasks. The Instruct scores on the unseen evaluation suite are shown in Table 24."
---

# Table 20

## Caption
Finally, we evaluate OLMo 2-Instruct on the unseen evaluation suite from Lambert et al. (2024) without the code evaluation tasks. The Instruct scores on the unseen evaluation suite are shown in Table 24.

## Data

| Hyperparameter                 | RLVRvalue                                                     |
|--------------------------------|---------------------------------------------------------------|
| Learning rate                  | 3 ⋅ 10 - 7 for 13B; 4 ⋅ 10 - 7 for 7B                         |
| Effective batch size           | 248 for 13B; 224 for 7B                                       |
| KL penalty coef. ( β )         | 0.1 for first and final 13B; 0.03 for second 13B; 0.05 for 7B |
| Max total episodes             | 200,000 for 13B; 100,000 for 7B                               |
| Discount factor γ              | 1.0                                                           |
| General advantage estimation λ | 0.95                                                          |
| Mini-batches N mb              | 1                                                             |
| PPO update iterations K        | 4                                                             |
