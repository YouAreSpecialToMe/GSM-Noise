from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        stories = []
        irrelative_informations = []

        names = ["Daniel", "Caleb", "Nathan", "Eli", "Hunter"]
        items = ["chocolate bars", "lollipops", "gummy bears", "caramel chews", "peppermint mints", "candy"]

        name = random.choice(names)
        item = random.choice(items)

        num1 = random.randint(1, 150)  # 初始订购的数量
        num2 = random.randint(0, num1 + 150)  # 卖出的数量，范围扩大以确保合理
        num3 = random.randint(1, 150)  # 后来又订购的数量

        total_candies = num1 + num3  # 总共订购的数量
        candies_left_to_sell = total_candies - num2  # 剩余需要卖出的数量

        if candies_left_to_sell >= 0:
            # 分解问题为句子级别
            story_1 = f"""{name} is selling {item} to raise money for {name}'s club at school."""
            stories.append(story_1)

            story_2 = f"""{name} doesn't have the {item} yet and is instead just taking orders."""
            stories.append(story_2)

            story_3 = f"""{name} started off with {num1} total that {name} ordered and wanted to sell."""
            stories.append(story_3)

            story_4 = f"""{name} ended up selling {num2} {item}."""
            stories.append(story_4)

            story_5 = f"""Then, {name} ordered {num3} more."""
            stories.append(story_5)

            original_problem = stories.copy()

            # 主题相关的无关信息
            num9 = random.randint(1, 3)
            irrelative_info_3 = f"""{name} has {num9} pair of binoculars that {name} uses to count the {item}."""
            irrelative_informations.append(irrelative_info_3)

            num8 = random.randint(20, 30)
            irrelative_info_4 = f"""The counting spot was in a park with {num8} trees and open spaces."""
            irrelative_informations.append(irrelative_info_4)

            # 主题无关的无关信息
            num7 = random.randint(2, 4)
            irrelative_info_1 = f"""{name} has {num7} pet dogs that often joins {name} on these outdoor trips."""
            irrelative_informations.append(irrelative_info_1)

            for irrelative_information in irrelative_informations:
                if random.random() < prob_irre:
                    stories.append(irrelative_information)

            first_story = stories[0]
            remaining_stories = stories[1:]
            if shuffle:
                random.shuffle(remaining_stories)
            stories = [first_story] + remaining_stories

            # 添加符号或语法错误
            stories_with_errors = []
            for p in stories:
                modified_sentence = introduce_grammar_error(p, prob_grammar_error)
                modified_sentence = introduce_symbol_error(modified_sentence, prob_symbol_error)
                stories_with_errors.append(modified_sentence)
            stories = stories_with_errors

            question = f"""How many does {name} still need to sell to sell all of his {item}?"""
            original_problem.append(question)
            stories.append(question)
            ans = candies_left_to_sell
            break

    # 返回问题和答案
    cot = [
        f"{name} started with {num1} {item} and then ordered {num3} more, making the total {item} {total_candies}.",
        f"{name} sold {num2} {item}, so the number of {item} left to sell is {total_candies} - {num2}, which is {candies_left_to_sell}."
    ]

    return {
        "cot": cot,
        "problem": stories,
        "answer": ans,
        "original_problem": original_problem,
        "irrelevant_infos": irrelative_informations
    }