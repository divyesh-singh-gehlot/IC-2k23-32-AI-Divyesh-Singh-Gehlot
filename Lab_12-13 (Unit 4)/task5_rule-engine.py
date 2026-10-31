# Part 5: Rule Engine (forward chaining)
# Each rule is ([conditions], conclusion).
# Keep applying rules until no new fact can be added.

medical_rules = [
    (["fever", "cough"], "suspect_flu"),
    (["suspect_flu", "body_ache"], "diagnosis_flu"),
    (["diagnosis_flu"], "advise_rest_and_fluids"),
    (["fever", "chills", "sweating"], "suspect_malaria"),
    (["suspect_malaria"], "advise_blood_test"),
]

university_rules = [
    (["attendance_ok", "assignments_done"], "eligible_for_exam"),
    (["eligible_for_exam", "passed_exam"], "course_completed"),
    (["course_completed", "credits_sufficient"], "eligible_for_graduation"),
]


def forward_chain(rules, known):
    facts = list(known)
    fired = []
    changed = True
    while changed:
        changed = False
        for conditions, conclusion in rules:
            if conclusion in facts:
                continue
            # check that every condition is already known
            all_true = True
            for c in conditions:
                if c not in facts:
                    all_true = False
            if all_true:
                facts.append(conclusion)
                fired.append((conditions, conclusion))
                changed = True
    return facts, fired


def run(title, rules, start_facts):
    print("---", title, "---")
    print("Starting facts:", start_facts)
    facts, fired = forward_chain(rules, start_facts)
    print("\nRules used:")
    for i, (conditions, conclusion) in enumerate(fired, 1):
        print(" ", str(i) + ".", "IF", " AND ".join(conditions), "THEN", conclusion)
    print("\nNew facts:", [f for f in facts if f not in start_facts])
    print()


run("Medical rules", medical_rules, ["fever", "cough", "body_ache"])
run("University rules", university_rules,
    ["attendance_ok", "assignments_done", "passed_exam", "credits_sufficient"])