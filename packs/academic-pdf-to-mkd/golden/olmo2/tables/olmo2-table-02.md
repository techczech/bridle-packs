---
type: table
table_id: "02"
paper_key: "olmo2"
data_file: "olmo2-table-02.csv"
caption: "Table 1 Summary of how OLMo family model architectures have evolved over time. Latest OLMo 2 changes were motivated by experiments showing improved training stability. Full descriptions in §2.1."
---

# Table 02

## Caption
Table 1 Summary of how OLMo family model architectures have evolved over time. Latest OLMo 2 changes were motivated by experiments showing improved training stability. Full descriptions in §2.1.

## Data

|                         | OLMo1(0224)    | OLMo-0424      | OLMo2    |
|-------------------------|----------------|----------------|----------|
| Biases                  | None           | None           | None     |
| Activation              | SwiGLU         | SwiGLU         | SwiGLU   |
| RoPE θ                  | 1 ⋅ 10 4       | 1 ⋅ 10 4       | 5 ⋅ 10 5 |
| QKVNormalization        | None           | Clip to 8      | QK-Norm  |
| LayerNorm               | non-parametric | non-parametric | RMSNorm  |
| Layer NormApplied to    | Inputs         | Inputs         | Outputs  |
| Z-Loss Weight           | 0              | 0              | 10 - 5   |
| WeightDecayonEmbeddings | Yes            | Yes            | No       |
