from student.models import Student, Question, Goal, Interest


def calculate_vark_model(responses):
    scores = {
        'Visual': 0,
        'Aural': 0,
        'Reading': 0,
        'Kinesthetic': 0
    }

    option_scores = {
        '0': 1,
        '1': 2,
        '2': 3,
        '3': 4
    }

    vark_question_mapping = {
        1: {
            1: 'Kinesthetic',
            2: 'Aural',
            3: 'Reading',
            4: 'Visual'
            },
        2: {
            1: 'Visual',
            2: 'Aural',
            3: 'Reading',
            4: 'Kinesthetic'
            },
        3:  {
            1: 'Kinesthetic',
            2: 'Visual',
            3: 'Reading',
            4: 'Aural'
            },
        4: {
            1: 'Kinesthetic',
            2: 'Aural',
            3: 'Visual',
            4: 'Reading'
            },
        5: {
            1: 'Aural',
            2: 'Visual',
            3: 'Kinesthetic',
            4: 'Reading'
            },
        6: {
            1: 'Kinesthetic',
            2: 'Reading',
            3: 'Visual',
            4: 'Aural',
            },
        7: {
            1: 'Kinesthetic',
            2: 'Aural',
            3: 'Visual',
            4: 'Reading',
            },
        8: {
            1: 'Reading',
            2: 'Kinesthetic',
            3: 'Aural',
            4: 'Visual',
            },
        9: {
            1: 'Reading',
            2: 'Aural',
            3: 'Kinesthetic',
            4: 'Visual',
            },
        10: {
            1: 'Kinesthetic',
            2: 'Visual',
            3: 'Reading',
            4: 'Aural',
            },
        11: {
            1: 'Visual',
            2: 'Reading',
            3: 'Aural',
            4: 'Kinesthetic',
        },
        12: {
            1: 'Aural',
            2: 'Reading',
            3: 'Visual',
            4: 'Kinesthetic',
        },
        13: {
            1: 'Kinesthetic',
            2: 'Aural',
            3: 'Reading',
            4: 'Visual',
        },
        14: {
            1: 'Kinesthetic',
            2: 'Reading',
            3: 'Aural',
            4: 'Visual',
        },
        15: {
            1: 'Kinesthetic',
            2: 'Aural',
            3: 'Reading',
            4: 'Visual',
        },
        16: {
            1: 'Visual',
            2: 'Aural',
            3: 'Reading',
            4: 'Kinesthetic'
            },
    }

    for question, responses in responses.items():
        learning_style = vark_question_mapping[int(question)+1]
        for response in responses:
            choice = response + 1
            scores[learning_style[choice]] += 1

    dominant_style = max(scores, key=scores.get)

    return  dominant_style.replace('"','')

def calculate_level_model(responses):
    question_mapping = {
     1: 3,
     2: 4,
     3: 2,
     4: 3,
     5: 1,
     6: 3,
     7: 3,
     8: 3,
     9: 3,
     10: 3,
     11: 2,
     12: 3,
     13: 4
    }
    total_score = 0
    for question_number, response in responses.items():
        correct_choice = question_mapping.get(int(question_number)+1)
        if correct_choice is not None and response[0] +1 == correct_choice:
            total_score += 1
    if total_score <= 5:
        user_level = "LowLevel"
    elif total_score <= 10:
        user_level = "MediumLevel"
    else:
        user_level = "AdvancedLevel"
    return user_level

def prepare_data_for_curricula(responses):
    interests = [Interest.objects.get(pk=pk).name for pk in responses["interests"]]
    goals = [Goal.objects.get(pk=pk).name for pk in responses["goals"]]
    personal_data = {
        "pk": responses["pk"],
        "level": responses["level"],
        "interests": interests,
        "goals": goals
    }
    return personal_data


def get_student_models():
    visual = 0
    auditory = 0
    reading = 0
    kinesthetic = 0
    all_students =  Student.objects.all().count()
    for student in  Student.objects.all():
        vark_model = student.vark_model.replace('"', '')
        if vark_model == "Visual":
            visual += 1
        elif vark_model == "Aural":
            auditory += 1
        elif vark_model == "Reading":
            reading += 1
        elif vark_model == "Kinesthetic":
            kinesthetic += 1
    response =[
        { "vark": 'Visual', "count": (visual/all_students) * 100},
        { "vark": 'Auditory', "count": (auditory/all_students) * 100},
        { "vark": 'Reading', "count": (reading/all_students) * 100},
        { "vark": 'Kinesthetic', "count": (kinesthetic/all_students) * 100 },
    ]
    return response