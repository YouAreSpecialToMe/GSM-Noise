from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define variables and assign random values
    
        # Possible numbers of students
        num_students_list = [10, 15, 20, 25, 30, 35, 40, 45, 50]
        num_students = random.choice(num_students_list)
    
        # Total amount raised, in $25,000 increments between $50,000 and $500,000
        total_raised = random.randint(2, 20) * 25000  # Generates between $50,000 and $500,000
    
        # Organizations' contribution: between $10,000 and total_raised - $10,000
        min_org_contribution = 10000
        max_org_contribution = total_raised - 10000
        org_contribution_options = [i for i in range(min_org_contribution, max_org_contribution + 1, 10000)]
        org_contribution = random.choice(org_contribution_options)
    
        # Ensure amount from students is positive
        amount_from_students = total_raised - org_contribution
    
        # Amount each student raised
        # Formula: amount_per_student = (total_raised - org_contribution) / num_students
        amount_per_student = amount_from_students / num_students
    
        # Choose a charity name
        charity_names = [
            'Children Hope Fund',
            'Global Aid Foundation',
            'Save the Earth Initiative',
            'Health and Wellness Foundation',
            'Education for All'
        ]
        charity_name = random.choice(charity_names)
    
        # Generate in-topic irrelevant information
        years = [1990, 1995, 2000, 2005, 2010, 2015]
        year_established = random.choice(years)
    
        founder_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley']
        founder_name = random.choice(founder_names)
    
        # Generate out-topic irrelevant information
        student_names = ['John', 'Emily', 'Michael', 'Sarah', 'David', 'Jessica']
        student_name = random.choice(student_names)
        student_age = random.randint(10, 18)
    
        # Construct the premise content, replacing values with variable names
        problem = [
            f"{num_students} students are working together to raise money for {charity_name}.",
            f"Each student earns the same amount.",
            f"{charity_name} raises a total of ${total_raised}.",
            f"${org_contribution} comes from organizations and the rest from the students."
        ]
    
        # Construct the question
        question = "How much did each student raise?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Add in-topic irrelevant information
        in_topic_irrelevants = [
            f"{charity_name} was established in {year_established} by {founder_name}.",
            "The organizations that contributed are well-known in the community."
        ]
    
        # Add out-topic irrelevant information
        out_topic_irrelevants = [
            f"{student_name} is one of the students and is {student_age} years old.",
            f"{student_name} enjoys playing soccer in their free time."
        ]
    
        # Combine irrelevant information
        irrelevant_infos = in_topic_irrelevants + out_topic_irrelevants
    
        # Randomly add irrelevant information based on probability
        for irre_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irre_info)
    
        # Apply symbol or grammar errors to the problem sentences
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            )
            for sentence in problem
        ]
    
        # Shuffle the order of sentences, except for the first one
        if shuffle:
            random.shuffle(problem[1:])
    
        # Add the question to the problem
        problem.append(question)
    
        # Calculate the answer using formula
        # amount_from_students = total_raised - org_contribution
        # answer = amount_from_students / num_students
        answer = amount_per_student
        if answer%1==0:
            break


    # Return the problem and answer as a dictionary
    cot = [f"The total amount raised by the students is {total_raised} - {org_contribution}, which is {amount_from_students}.", f"Each student raised {amount_from_students} / {num_students}, which is {amount_per_student}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

