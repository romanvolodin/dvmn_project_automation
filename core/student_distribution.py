def count_avaliable_slots(product_managers):
    avaliable_slots = {}

    for manager_name, manager_slots in product_managers.items():
        for slot in manager_slots:
            if slot in avaliable_slots:
                avaliable_slots[slot].append(manager_name)
            else:
                avaliable_slots[slot] = [manager_name]

    return avaliable_slots


# def count_students_per_slot(slots, students):
#     students_per_slot = {}
#     for slot in slots.keys():
#         students_per_slot[slot] = 0
#         for student_slots in students.values():
#             if slot in student_slots:
#                 students_per_slot[slot] += 1
#     return students_per_slot


# def count_students_per_slot2(slots, students):
#     students_per_slot = {}
#     for slot in slots.keys():
#         students_per_slot[slot] = 0
#         for category, category_students in students.items():
#             for student_slots in category_students.values():
#                 if slot in student_slots:
#                     students_per_slot[slot] += 1
#     return students_per_slot


def distribute_students(students, product_managers, limit=3):
    teams = {}

    for level, level_students in students.items():
        distributed_students = []
        prioritized_students = dict(
            sorted(level_students.items(), key=lambda student: len(student[1]))
        )
        for student_name, student_slots in prioritized_students.items():
            if student_name in distributed_students:
                continue
            for slot in student_slots:
                if student_name in distributed_students:
                    continue
                if slot not in teams:
                    teams[slot] = [[]]
                if len(teams[slot][-1]) >= limit:
                    teams[slot].append([])
                current_team_slot = teams[slot][-1]
                current_team_slot.append(student_name)
                distributed_students.append(student_name)

                for teammate_name, teammate_slots in prioritized_students.items():
                    if teammate_name in distributed_students:
                        continue
                    if slot in teammate_slots:
                        current_team_slot.append(teammate_name)
                        distributed_students.append(teammate_name)
                    if len(current_team_slot) >= limit:
                        break
                break

        # ?????????????????? ???????????? ??????????????, ?????????? ?????????????? ???? ?????????????????????? ?? ????????????
        for slot in teams:
            teams[slot].append([])

    return teams


if __name__ == "__main__":
    students = {
        "junior": {
            "?????????????? ??????????": [
                # "19:30",
                "20:00",
                "20:30",
            ],
            "?????????? ??????????????": [
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
            "????????": [
                "18:00",
                "18:30",
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
            "?????????????? ????????????": [
                "18:00",
                "18:30",
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
            "???????????? Nori": [
                "18:00",
                "18:30",
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
            "?????????????? ????????????": [
                "18:00",
                "18:30",
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
            "?????????????? ??????????????????": [
                "18:00",
                "18:30",
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
        },
        "beginner+": {
            "?????????????????? ??????": [
                # "8:00",
                # "8:30",
                # "9:00",
                # "9:30",
                # "10:00",
                # "10:30",
                "17:00",
                "17:30",
            ],
            "?????????? ??????????????????": [
                "17:00",
                "17:30",
            ],
            "?????????? ????????????": [
                "18:00",
                "18:30",
                "19:00",
                "19:30",
            ],
            "?????????????????? ????????": [
                "17:00",
                # "18:00",
            ],
            "?????????????? ??????????????????": [
                "17:00",
                "17:30",
                "18:00",
                "18:30",
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
            "?????????????? ??????????????": [
                "17:00",
                "17:30",
                "18:00",
                "18:30",
                "19:00",
                "19:30",
                "20:00",
                "20:30",
            ],
            "???????? ????????????????????????": [],
        },
        "beginner": {
            "???????????? ??????????????": [
                "17:00",
                "17:30",
                "18:00",
                "18:30",
            ],
            "???????? ????????????????": [
                # "20:15",
                "20:00",
            ],
            "?????????????????? ??????????????????": [
                "19:30",
            ],
            "?????????????? ????????????????": [
                "19:30",
            ],
        },
    }

    product_managers = {
        "????????": [
            "8:00",
            "8:30",
            "9:00",
            "9:30",
            "19:00",
            "19:30",
            "20:00",
            "20:30",
        ],
        "??????": [
            "18:00",
            "18:30",
            "19:00",
            "19:30",
        ],
    }

    from pprint import pprint

    pprint(distribute_students(students, product_managers))
