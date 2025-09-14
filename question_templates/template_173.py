from grammar_error import introduce_grammar_error, introduce_symbol_error

import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # 原始问题中的变量
    name = "Jane"
    plant = "beanstalk"
    init_height = 3
    action_week2_type = 'multiply'  # 'multiply' 或 'add'
    growth_factor_week2 = 2
    added_height_week2 = 0  # 初始化 added_height_week2
    added_height_week3 = 4
    total_weeks = 3
    ground_truth_answer = 10

    # 使用原始值计算答案
    height_week1 = init_height
    if action_week2_type == 'multiply':
        height_week2 = height_week1 * growth_factor_week2
    else:
        height_week2 = height_week1 + added_height_week2
    height_week3 = height_week2 + added_height_week3
    calculated_answer = height_week3

    # 定义可选值并随机化变量
    names = ["Alice", "Bob", "Carlos", "Daisy", "Eve", "Frank", "Jane"]
    plants = ["beanstalk", "sunflower", "corn plant", "bamboo", "cactus"]
    init_heights = list(range(1, 10))
    action_week2_types = ['multiply', 'add']
    growth_factors_week2 = [2, 3, 4]
    added_heights_week2 = list(range(1, 15))
    added_heights_week3 = list(range(1, 15))
    total_weeks = 3

    # 随机分配变量
    name = random.choice(names)
    plant = random.choice(plants)
    init_height = random.choice(init_heights)
    action_week2_type = random.choice(action_week2_types)
    if action_week2_type == 'multiply':
        growth_factor_week2 = random.choice(growth_factors_week2)
        added_height_week2 = 0  # 确保 added_height_week2 被定义
        if growth_factor_week2 == 2:
            action_week2_sentence = f"It doubled in height the second week."
        elif growth_factor_week2 == 3:
            action_week2_sentence = f"It tripled in height the second week."
        else:
            action_week2_sentence = f"It became {growth_factor_week2} times taller the second week."
    else:
        added_height_week2 = random.choice(added_heights_week2)
        growth_factor_week2 = 1  # 确保 growth_factor_week2 被定义
        action_week2_sentence = f"It grew another {added_height_week2} inches in the second week."
    added_height_week3 = random.choice(added_heights_week3)

    # 构建问题句子
    problem = [
        f"{name} planted a {plant} in {name}'s backyard.",
        f"After the first week, it was {init_height} inches tall.",
        action_week2_sentence,
        f"It grew another {added_height_week3} inches in the third week."
    ]

    # 构建问题
    question = f"How tall was the {plant} after {total_weeks} weeks?"
    original_problem = problem.copy()
    original_problem.append(question)

    # 添加主题相关的无关信息
    in_topic_irrelevant_infos = [
        f"The {plant} needs water every day.",
        f"{name} also grows roses in the backyard.",
        f"The {plant} requires plenty of sunlight.",
        f"{name}'s backyard is very large."
    ]
    # 添加主题无关的无关信息
    all_jobs = ["teacher", "engineer", "artist", "doctor", "chef"]
    job = random.choice(all_jobs)
    out_topic_irrelevant_info = f"{name} works as a {job} in the city."
    irrelevant_infos = in_topic_irrelevant_infos + [out_topic_irrelevant_info]

    # 随机添加无关信息
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # 添加符号或语法错误（假设函数已给出）
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # 打乱句子顺序，除第一句外
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # 添加问题
    problem.append(question)

    # 计算答案
    height_week1 = init_height
    if action_week2_type == 'multiply':
        height_week2 = height_week1 * growth_factor_week2
    else:
        height_week2 = height_week1 + added_height_week2
    height_week3 = height_week2 + added_height_week3
    answer = height_week3

    # 构建解题过程（cot）
    if action_week2_type == 'multiply':
        cot = [
            f"After the first week, the {plant} was {init_height} inches tall.",
            f"In the second week, it multiplied in height by {growth_factor_week2}, so {height_week2} = {init_height} * {growth_factor_week2}.",
            f"In the third week, it grew another {added_height_week3} inches, so {height_week3} = {height_week2} + {added_height_week3}.",
            f"Therefore, the height of the {plant} after {total_weeks} weeks is {height_week3} inches."
        ]
    else:
        cot = [
            f"After the first week, the {plant} was {init_height} inches tall.",
            f"In the second week, it grew by {added_height_week2} inches, so {height_week2} = {init_height} + {added_height_week2}.",
            f"In the third week, it grew another {added_height_week3} inches, so {height_week3} = {height_week2} + {added_height_week3}.",
            f"Therefore, the height of the {plant} after {total_weeks} weeks is {height_week3} inches."
        ]

    return {
        "cot": cot,
        'problem': problem,
        'answer': answer,
        'original_problem': original_problem,
        'irrelevant_infos': irrelevant_infos
    }