---
type: table
table_id: "12"
paper_key: "olmo2"
data_file: "olmo2-table-12.csv"
caption: "Table 10 A summary of high-quality sources we evaluate for mid-training. We experiment with mixing these sources in 6 mixes, each consisting of 50 billion tokens. Percentages on the table indicate the fraction of each 50B mix that is comprised by data from the respective source. PT Mix is sampled (with repetition) from the pretraining stage."
---

# Table 12

## Caption
Table 10 A summary of high-quality sources we evaluate for mid-training. We experiment with mixing these sources in 6 mixes, each consisting of 50 billion tokens. Percentages on the table indicate the fraction of each 50B mix that is comprised by data from the respective source. PT Mix is sampled (with repetition) from the pretraining stage.

## Data

| Source    |                 |                               | Mix%            | Mix%          | Mix%          | Mix%                 | Mix%                | Mix%                       |
|-----------|-----------------|-------------------------------|-----------------|---------------|---------------|----------------------|---------------------|----------------------------|
|           |                 |                               | PT Mix Web FT 7 | Web FT 7 FW 3 | Web FT 7 FW 2 | Web FT 7 FW 2 + Math | Web FT 7 FW 2 + Ins | Web FT 7 FW 2 + Math + Ins |
| DCLM      | from pretrain   | 95.2                          | -               | -             | -             | -                    | -                   | -                          |
| DCLM WEB  | FT top          | 7%                            | - 57.1          | -             | -             | -                    | -                   | -                          |
|           | DCLM            | FT top 7% FineWeb ⩾ 3         | - -             | 54.2          | -             | -                    | -                   | -                          |
|           | DCLM            | FT top 7% FineWeb ⩾ 2         | -               | - -           | 57.9          | 61.8                 | 75.5                | 57.5                       |
| INST      | Flan            | Dolma 1.7 decontaminated      | -               | - -           | -             | -                    | 8.8                 | 6.7                        |
|           | Stack Exchange  | 2024/09/30 dump Q&A format    | -               | - -           | -             | -                    | 0.7                 | 0.5                        |
| CODE      | Starcoder       | from pretrain                 | 2.1             | 19.5 20.9     | 19.2          | -                    | -                   | -                          |
| CODE      | CodeSearchNet   | unfiltered                    | -               | - -           | -             | 0.1                  | 0.2                 | 0.1                        |
| CODE      | Gutenberg Books | from Dolma 1.7                | -               | 1.2 1.3       | 1.2           | -                    | -                   | -                          |
|           | peS2o           | from pretrain                 | 1.5 6.6         | 7.1           | 6.5           | 10.7                 | 13.0                | 9.9                        |
| REFERENCE | Wikipedia       | from pretrain                 | 0.1             | 0.9 0.9       | 0.9           | 1.6                  | 1.9                 | 1.4                        |
|           | StackExchange   | from RedPajama v1             | -               | 4.0 4.3       | 4.0           | -                    | -                   | -                          |
|           | ArXiv           | from pretrain                 | 0.5             | 4.9 5.2       | 4.8           | -                    | -                   | -                          |
|           | Algebraic Stack | from pretrain                 | 0.3             | 2.8 3.0       | 2.7           | -                    | -                   | -                          |
|           | OpenWebMath     | from pretrain                 | 0.3             | 2.9 3.1       | 2.8           | 5.2                  | -                   | 4.8                        |
| MATH      | GSM8k           | train split                   | -               | - 0.003       | 0.003         | 0.003                | -                   | 0.003                      |
|           | Mathpile        | commercial subset train split | -               | - -           | -             | 2.1                  | -                   | 1.9                        |
|           | AutoMathText    | unfiltered                    | -               | - -           | -             | 18.5                 | -                   | 17.2                       |
