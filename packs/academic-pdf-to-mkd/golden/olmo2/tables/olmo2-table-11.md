---
type: table
table_id: "11"
paper_key: "olmo2"
data_file: "olmo2-table-11.csv"
caption: "Table 9 Evaluations comparing OLMo 2 1B, 7B, 13B and 32B at the end of pretraining and mid-training stages (setup mirrors Table 6). Pretrain checkpoints have been trained on 4 trillion (1B, 7B), 5 trillion (13B) and 7 trillion (32B) tokens respectively. For 7B, we obtain the final mid-train checkpoints by averaging three training runs on 50B Dolmino tokens; for 13B and 32B, we use three runs on 100B tokens and one run on 300B tokens. For 1B, the final checkpoint is the result of training on 50B Dolmino tokens without averaging."
---

# Table 11

## Caption
Table 9 Evaluations comparing OLMo 2 1B, 7B, 13B and 32B at the end of pretraining and mid-training stages (setup mirrors Table 6). Pretrain checkpoints have been trained on 4 trillion (1B, 7B), 5 trillion (13B) and 7 trillion (32B) tokens respectively. For 7B, we obtain the final mid-train checkpoints by averaging three training runs on 50B Dolmino tokens; for 13B and 32B, we use three runs on 100B tokens and one run on 300B tokens. For 1B, the final checkpoint is the result of training on 50B Dolmino tokens without averaging.

## Data

|                            | Dev Benchmarks   | Dev Benchmarks   | Dev Benchmarks   | Dev Benchmarks   | Dev Benchmarks   | Dev Benchmarks   | Dev Benchmarks   | Held-out Evals   | Held-out Evals   | Held-out Evals   | Held-out Evals   |
|----------------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
| Checkpoint                 | Avg              | MMLU             | ARC C            | HSwag            | WinoG            | NQ               | DROP             | AGIEval          | GSM8K            | MMLU PRO         | TQA              |
| OLMo21B                    | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          | OLMo21B          |
| Pretraining                | 31.9             | 26.9             | 26.1             | 67.5             | 67.8             | 16.1             | 25.1             | 24.5             | 3.3              | 11.1             | 50.1             |
| Pretraining & mid-training | 43.7             | 44.3             | 51.3             | 69.5             | 66.5             | 20.8             | 34.0             | 36.3             | 43.8             | 16.1             | 54.7             |
| OLMo27B                    | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          | OLMo27B          |
| Pretraining                | 53.0             | 59.8             | 72.6             | 81.3             | 75.8             | 29.0             | 40.7             | 44.6             | 24.1             | 27.4             | 74.6             |
| Pretraining & mid-training | 62.9             | 63.7             | 79.8             | 83.8             | 77.2             | 36.9             | 60.8             | 50.4             | 67.5             | 31.0             | 78.0             |
| OLMo213B                   | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         | OLMo213B         |
| Pretraining                | 58.9             | 63.4             | 80.2             | 84.8             | 79.4             | 34.6             | 49.6             | 48.2             | 37.3             | 31.2             | 80.3             |
| Pretraining & mid-training | 68.3             | 67.5             | 83.5             | 86.4             | 81.5             | 46.7             | 70.7             | 54.2             | 75.1             | 35.1             | 81.9             |
| OLMo232B                   | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         | OLMo232B         |
| Pretraining                | 66.3             | 72.9             | 88.7             | 84.2             | 82.4             | 40.6             | 57.2             | 56.8             | 56.2             | 38.5             | 85.4             |
| Pretraining & mid-training | 73.3             | 74.9             | 90.4             | 89.7             | 83.0             | 50.2             | 74.3             | 61.0             | 78.8             | 43.3             | 88.0             |
