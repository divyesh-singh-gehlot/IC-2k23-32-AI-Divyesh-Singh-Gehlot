# Part 1: University Knowledge Base
# Facts are stored as tuples like (predicate, arg1, arg2)

facts = [
    ("professor", "Dr_Rao"), ("professor", "Dr_Mehta"), ("professor", "Dr_Khan"),
    ("works_in", "Dr_Rao", "CSE"), ("works_in", "Dr_Mehta", "Maths"), ("works_in", "Dr_Khan", "CSE"),
    ("teaches", "Dr_Rao", "AI"), ("teaches", "Dr_Khan", "DBMS"), ("teaches", "Dr_Mehta", "Calculus"),
    ("enrolled_in", "Asha", "AI"), ("enrolled_in", "Asha", "DBMS"),
    ("enrolled_in", "Ravi", "AI"), ("enrolled_in", "Ravi", "Calculus"),
    ("enrolled_in", "Meena", "Calculus"),
]


def find(predicate, first=None, second=None):
    # None means "any value" (acts like a variable)
    answers = []
    for fact in facts:
        if fact[0] != predicate:
            continue
        if first is not None and fact[1] != first:
            continue
        if len(fact) > 2 and second is not None and fact[2] != second:
            continue
        answers.append(fact)
    return answers


print("Total facts:", len(facts))

print("\nWho teaches AI?")
for f in find("teaches", None, "AI"):
    print(" ", f[1])

print("\nCourses taken by Asha:")
for f in find("enrolled_in", "Asha"):
    print(" ", f[2])

print("\nStudents enrolled in AI:")
for f in find("enrolled_in", None, "AI"):
    print(" ", f[1])

# combining two facts: students taught by Dr_Rao
print("\nStudents taught by Dr_Rao:")
students = []
for t in find("teaches", "Dr_Rao"):
    course = t[2]
    for e in find("enrolled_in", None, course):
        if e[1] not in students:
            students.append(e[1])
print(" ", students)