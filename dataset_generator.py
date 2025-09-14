import importlib
import random
import os
import json
from tqdm import tqdm
from fractions import Fraction

def generate_samples(nums, template_indices, dataset_name, prob_irre, prob_grammar_error, prob_symbol_error, shuffle, output_path):
    samples = []
    print(f"Processing file: {dataset_name}.jsonl")
    for idx in tqdm(template_indices, desc=f"Generating samples for {dataset_name}"):
        module_name = f'template_{idx}'
        try:
            # Dynamically import template module
            template_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(f"Module {module_name} not found.")
            continue

        # Get generate_new_problem function
        generate_new_problem = getattr(template_module, 'generate_new_problem')

        # Generate 50 samples per template
        for _ in range(nums):
            sample = generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle)
            samples.append(sample)

    # Save samples to file
    save_samples(samples, dataset_name, output_path)

def save_samples(samples, dataset_name, output_path):
    has_fraction = any(isinstance(value, Fraction) for sample in samples for value in sample.values())

    filename = f'{dataset_name}.jsonl'
    full_path = os.path.join(output_path, filename)

    with open(full_path, 'a', encoding='utf-8') as f:
        for sample in samples:
            converted_sample = {
                'cot': [str(item) if isinstance(item, Fraction) else item for item in sample['cot']] if isinstance(
                    sample['cot'], list) else str(sample['cot']) if isinstance(sample['cot'], Fraction) else sample[
                    'cot'],
                'problem': [str(item) if isinstance(item, Fraction) else item for item in
                            sample['problem']] if isinstance(sample['problem'], list) else str(
                    sample['problem']) if isinstance(sample['problem'], Fraction) else sample['problem'],
                'answer': str(sample['answer']) if isinstance(sample['answer'], Fraction) else sample['answer'],
                'original_problem': [str(item) if isinstance(item, Fraction) else item for item in
                                     sample['original_problem']] if isinstance(sample['original_problem'],
                                                                               list) else str(
                    sample['original_problem']) if isinstance(sample['original_problem'], Fraction) else sample[
                    'original_problem'],
                'irrelevant_infos': [str(item) if isinstance(item, Fraction) else item for item in
                                     sample['irrelevant_infos']] if isinstance(sample['irrelevant_infos'],
                                                                               list) else str(
                    sample['irrelevant_infos']) if isinstance(sample['irrelevant_infos'], Fraction) else sample[
                    'irrelevant_infos']
            }

            json.dump(converted_sample, f)

    print(f"Dataset is save to {full_path}")


if __name__ == '__main__':
    # Set probabilities using command line arguments or defaults
    import argparse

    parser = argparse.ArgumentParser(description="Generate a dataset.")
    parser.add_argument('--prob_irre', type=float, default=1, help="Probability of adding irrelevant information.")
    parser.add_argument('--prob_grammar_error', type=float, default=0.4, help="Probability of adding grammar errors.")
    parser.add_argument('--prob_symbol_error', type=float, default=0.015, help="Probability of adding meaningless symbols.")
    parser.add_argument('--shuffle', type=bool, default=True, help="Shuffle the templates before splitting.")
    parser.add_argument('--num', type=int, default=50, help="Number of samples to generate per template.")
    parser.add_argument('--train_ratio', type=float, default=0.7, help="Proportion of templates used for training.")
    parser.add_argument('--val_ratio', type=float, default=0.15, help="Proportion of templates used for validation.")
    args = parser.parse_args()

    total_templates = 220
    template_indices = list(range(total_templates))

    # Validate ratios
    if not (0 < args.train_ratio < 1):
        raise ValueError("--train_ratio must be in (0, 1)")
    if not (0 <= args.val_ratio < 1):
        raise ValueError("--val_ratio must be in [0, 1)")
    if args.train_ratio + args.val_ratio >= 1:
        raise ValueError("train_ratio + val_ratio must be < 1")

    # Compute split indices
    train_split = int(args.train_ratio * total_templates)
    val_split = int((args.train_ratio + args.val_ratio) * total_templates)

    train_indices = template_indices[:train_split]
    val_indices = template_indices[train_split:val_split]
    test_indices = template_indices[val_split:]


    new_folder_name = ""
    is_first = True
    if args.prob_irre > 0:
        if is_first:
            new_folder_name += f"irre-{args.prob_irre}"
            is_first = False
        else:
            new_folder_name += f"_irre-{args.prob_irre}"

    if args.prob_grammar_error > 0:
        if is_first:
            new_folder_name += f"grammar-{args.prob_grammar_error}_symbol-{args.prob_symbol_error}"
            is_first = False
        else:
            new_folder_name += f"_grammar-{args.prob_grammar_error}_symbol-{args.prob_symbol_error}"

    if args.shuffle:
        if is_first:
            new_folder_name += f"shuffle"
            is_first = False
        else:
            new_folder_name += f"_shuffle"

    if not os.path.exists(new_folder_name):
        os.makedirs(new_folder_name)

    # Generate samples for each dataset split
    generate_samples(train_indices, 'train', args.prob_irre, args.prob_grammar_error, args.prob_symbol_error,
                     new_folder_name)
    generate_samples(val_indices, 'validation', args.prob_irre, args.prob_grammar_error, args.prob_symbol_error,
                     new_folder_name)
    generate_samples(test_indices, 'test', args.prob_irre, args.prob_grammar_error, args.prob_symbol_error,
                     new_folder_name)
