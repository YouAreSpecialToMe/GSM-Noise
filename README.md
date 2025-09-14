# GSM-Noise
This is the official GitHub repo of the **GSM-Noise** paper.

## Dataset Generator

This script generates synthetic math reasoning datasets with configurable noise (irrelevant information, grammar errors, and symbol errors). It dynamically loads problem templates (e.g., `template_0.py`, `template_1.py`, …) and saves the generated problems into JSONL files.

---

## Requirements

Make sure you have Python 3.8+ installed. Install dependencies:

```bash
pip install tqdm

---

## Usage

Run the script directly from the command line:

```bash
python generate_dataset.py \
    --prob_irre 1 \
    --prob_grammar_error 0.4 \
    --prob_symbol_error 0.015 \
    --shuffle True \
    --num 50

### Arguments

•	--prob_irre (float, default=1)
Probability of adding irrelevant information to problems.

	•	--prob_grammar_error (float, default=0.4)
Probability of introducing grammar errors.

	•	--prob_symbol_error (float, default=0.015)
Probability of inserting meaningless symbols.

	•	--shuffle (bool, default=True)
Whether to shuffle the question statements.

	•	--num (int, default=50)
Number of samples to generate per template.
