# 🧩 Lab 4 — Knowledge Representation & Logical Reasoning

## Overview

These lab represents knowledge in four ways (predicate facts, structured medical knowledge, semantic networks and frames) and then reasons over it with a rule engine. Each part is a small, separate program.

```text
Lab_4/
├── task1_university_kb.py
├── task2_medical_kr.py
├── task3_semantic_network.py
├── task4_frames.py
├── task5_rule_engine.py
├── outputs/
│   ├── Task1.png
│   ├── Task2.png
│   ├── Task3.png
│   ├── Task4.png
│   └── Task5.png
└── README.md
```

### Progress

- [x] Part 1: University Knowledge Base
- [x] Part 2: Medical Knowledge Representation
- [x] Part 3: Semantic Network
- [x] Part 4: Frame Representation
- [x] Part 5: Logical Rule Engine
- [x] Analysis: Frames vs Semantic Networks vs Rules

### How to Run

```bash
pip install networkx matplotlib
cd Lab_4
python task1_university_kb.py
python task2_medical_kr.py
python task3_semantic_network.py
python task4_frames.py
python task5_rule_engine.py
```

---

# 1. University Knowledge Base (Predicate Representation)

## 1.1 Aim / Problem Statement

### Aim
To represent university knowledge (professors, courses, students) as **predicate facts** and answer questions by querying and combining those facts.

### Problem Statement
Store facts about who works where, who teaches which course and who is enrolled in which course. Then:

1. answer simple questions (for example *who teaches AI?*), and
2. derive new knowledge by combining two kinds of facts (for example *which students are taught by Dr_Rao?*).

### Example
```text
teaches(Dr_Rao, AI)
enrolled_in(Asha, AI)
works_in(Dr_Rao, CSE)
```

## 1.2 Algorithm

**Representation:** every fact is a tuple `(predicate, argument1, argument2)`. The knowledge base is a list of 14 such facts:

| Predicate | Meaning | Facts |
|---|---|---|
| `professor(x)` | x is a professor | 3 |
| `works_in(x, d)` | professor x works in department d | 3 |
| `teaches(x, c)` | professor x teaches course c | 3 |
| `enrolled_in(s, c)` | student s is enrolled in course c | 5 |

**Querying:** `find(predicate, first, second)` scans the facts; passing `None` for an argument means "any value" (it behaves like a variable).

**Inference rule (written in logic):**

```text
taught_by(Student, Prof)  :-  teaches(Prof, Course)  AND  enrolled_in(Student, Course)
```

### Pseudocode
```text
find(predicate, first, second):
    FOR EACH fact in knowledge base:
        IF predicate differs: skip
        IF first is given AND differs: skip
        IF second is given AND differs: skip
        add fact to answers
    RETURN answers

students_taught_by(prof):
    FOR EACH (prof teaches course):
        FOR EACH (student enrolled_in course):
            add student to answer list (no duplicates)
```

## 1.3 Implementation

```python
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
```

## 1.4 Results / Output

```text
Total facts: 14

Who teaches AI?
  Dr_Rao

Courses taken by Asha:
  AI
  DBMS

Students enrolled in AI:
  Asha
  Ravi

Students taught by Dr_Rao:
  ['Asha', 'Ravi']
```

**Result:** all four questions are answered correctly. The last answer is a *derived* fact: no single stored fact says "Dr_Rao teaches Asha", but combining `teaches(Dr_Rao, AI)` with `enrolled_in(Asha, AI)` and `enrolled_in(Ravi, AI)` produces it.

## 1.5 Performance Analysis

| Metric | Result |
|---|---|
| Accuracy / Precision / Recall / F1 / Confusion Matrix | Not Applicable (not a classification problem) |
| Facts stored | 14 |
| Queries answered | 4 (3 direct, 1 derived) |
| Time Complexity | O(F) per `find()` call for F facts (linear scan); the derived query costs O(T x F) for T teaching facts |
| Space Complexity | O(F) |

A linear scan is fine for 14 facts. A larger knowledge base would index facts by predicate (for example a dictionary of lists) so that a query does not have to look at every fact.

## 1.6 Screenshots / Visualization

```text
Dr_Rao ──teaches──► AI ◄──enrolled_in── Asha
                     ▲
                     └──enrolled_in──── Ravi

Derived fact:  Dr_Rao ──(teaches, through AI)──► Asha, Ravi
```

Console screenshot:

![Console Output](outputs/Task1.png)

## 1.7 Learning Outcomes

* Represented knowledge as predicate facts with arguments.
* Wrote a query function where `None` acts as a wildcard variable.
* Derived new knowledge by joining two sets of facts (a simple logical rule).
* Understood why indexing matters when the knowledge base grows.

---

# 2. Medical Knowledge Representation

## 2.1 Aim / Problem Statement

### Aim
To represent medical knowledge (diseases, symptoms, treatments) in a structured form and rank the diseases that best explain a patient's symptoms.

### Problem Statement
Store a small medical knowledge base. Given the symptoms reported by a patient, list the possible diseases ordered by how many of that disease's symptoms were reported, together with the stored treatment.

> **Note:** this is an educational lab exercise, not medical advice.

### Example
```text
Patient symptoms: fever, cough, body_ache
```

## 2.2 Algorithm

**Representation:** a dictionary maps each disease to its knowledge:

```text
disease -> { symptoms: [list of symptoms], treatment: "text" }
```

The knowledge base holds 4 diseases: Flu, Common Cold, Malaria and Migraine.

**Matching score** for a disease:

```text
score = (number of patient symptoms found in the disease) / (total symptoms of the disease)
```

### Pseudocode
```text
FOR EACH disease in the knowledge base:
    count = number of patient symptoms that appear in the disease's symptom list
    IF count > 0:
        score = count / total symptoms of the disease
        add (score, disease) to results

Sort results from highest to lowest score
Display each disease with its score and treatment
```

## 2.3 Implementation

```python
# Part 2: Medical Knowledge Representation
# (only for lab practice, not real medical advice)

diseases = {
    "Flu": {
        "symptoms": ["fever", "cough", "body_ache", "fatigue"],
        "treatment": "Rest, fluids, antiviral if prescribed",
    },
    "Common Cold": {
        "symptoms": ["cough", "sneezing", "runny_nose", "sore_throat"],
        "treatment": "Rest and fluids",
    },
    "Malaria": {
        "symptoms": ["fever", "chills", "headache", "sweating"],
        "treatment": "Antimalarial medicine (see a doctor)",
    },
    "Migraine": {
        "symptoms": ["headache", "nausea", "light_sensitivity"],
        "treatment": "Rest in a dark room",
    },
}

print("Knowledge base:")
for name in diseases:
    print(name, "->", diseases[name]["symptoms"])

patient = ["fever", "cough", "body_ache"]
print("\nPatient symptoms:", patient)

results = []
for name in diseases:
    count = 0
    for s in patient:
        if s in diseases[name]["symptoms"]:
            count = count + 1
    if count > 0:
        score = count / len(diseases[name]["symptoms"])
        results.append((score, name))

results.sort(reverse=True)

print("\nPossible diseases:")
for score, name in results:
    print(name, "-", round(score * 100), "% match")
    print("   treatment:", diseases[name]["treatment"])
```

## 2.4 Results / Output

```text
Knowledge base:
Flu -> ['fever', 'cough', 'body_ache', 'fatigue']
Common Cold -> ['cough', 'sneezing', 'runny_nose', 'sore_throat']
Malaria -> ['fever', 'chills', 'headache', 'sweating']
Migraine -> ['headache', 'nausea', 'light_sensitivity']

Patient symptoms: ['fever', 'cough', 'body_ache']

Possible diseases:
Flu - 75 % match
   treatment: Rest, fluids, antiviral if prescribed
Malaria - 25 % match
   treatment: Antimalarial medicine (see a doctor)
Common Cold - 25 % match
   treatment: Rest and fluids
```

**Result:** Flu is the best match.

| Disease | Matched symptoms | Score |
|---|---|---|
| Flu | fever, cough, body_ache (3 of 4) | 75 % |
| Malaria | fever (1 of 4) | 25 % |
| Common Cold | cough (1 of 4) | 25 % |
| Migraine | none | not listed |

Malaria and Common Cold tie at 25 %. The program sorts `(score, name)` pairs in reverse order, so tied diseases appear in reverse alphabetical order.

## 2.5 Performance Analysis

| Metric | Result |
|---|---|
| Accuracy / Precision / Recall / F1 / Confusion Matrix | Not Applicable (not a classification problem) |
| Diseases in knowledge base | 4 |
| Patient symptoms | 3 |
| Best match | Flu (75 %) |
| Time Complexity | O(D x k x S) for D diseases, k patient symptoms and S symptoms per disease (small constants here) |
| Space Complexity | O(D x S) |

**Limitations:** the score only counts overlap. It ignores how rare or serious a symptom is, treats all symptoms as equally important, and cannot say "none of these". Real medical expert systems use weighted symptoms or probabilities.

## 2.6 Screenshots / Visualization

```text
Patient: fever, cough, body_ache

Flu          ████████████████████  75 %   (3 of 4 symptoms)
Malaria      ███████               25 %   (1 of 4 symptoms)
Common Cold  ███████               25 %   (1 of 4 symptoms)
```

Console screenshot:

![Console Output](outputs/Task2.png)

## 2.7 Learning Outcomes

* Represented domain knowledge with nested dictionaries.
* Built a simple matching score and understood its limits.
* Noticed tie-breaking behaviour caused by sorting tuples.
* Separated educational demos from real medical decision-making.

---

# 3. Semantic Network Construction

## 3.1 Aim / Problem Statement

### Aim
To build a **semantic network** of university concepts, show how properties are **inherited** along `is_a` links, and draw the network.

### Problem Statement
Represent concepts (Person, Student, Professor, Asha, Dr_Rao, AI_Course, ...) as nodes and the relationships between them as labelled edges. Then find which properties a particular student has, including properties inherited from more general concepts.

### Example
```text
Asha --instance_of--> Student --is_a--> Person
Student --has--> Roll_No
Person  --has--> Name
```

## 3.2 Algorithm

**Representation:** a directed graph (`networkx.DiGraph`). Nodes are concepts; every edge carries a relation label.

| Relation | Meaning |
|---|---|
| `is_a` | a class is a kind of a more general class |
| `instance_of` | an individual belongs to a class |
| `has` | a class has a property |
| `teaches`, `enrolled_in`, `works_in`, `offered_by` | relations between individuals |

**Inheritance:** to find the properties of a node, collect its own `has` links and then keep following `is_a` / `instance_of` links upward, collecting `has` links at each level.

### Pseudocode
```text
get_properties(node):
    to_visit = [node]
    WHILE to_visit is not empty:
        current = remove one node from to_visit
        FOR EACH outgoing edge (current -> next, relation):
            IF relation = "has":
                record property next (found at current)
            ELSE IF relation is "is_a" or "instance_of":
                add next to to_visit
    RETURN recorded properties
```

## 3.3 Implementation

```python
# Part 3: Semantic Network
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

g = nx.DiGraph()

# (from, to, relation)
relations = [
    ("Student", "Person", "is_a"),
    ("Professor", "Person", "is_a"),
    ("Person", "Name", "has"),
    ("Student", "Roll_No", "has"),
    ("Professor", "Employee_ID", "has"),
    ("Asha", "Student", "instance_of"),
    ("Ravi", "Student", "instance_of"),
    ("Dr_Rao", "Professor", "instance_of"),
    ("Dr_Rao", "AI_Course", "teaches"),
    ("Asha", "AI_Course", "enrolled_in"),
    ("Ravi", "AI_Course", "enrolled_in"),
    ("AI_Course", "CSE_Dept", "offered_by"),
    ("Dr_Rao", "CSE_Dept", "works_in"),
]

for a, b, rel in relations:
    g.add_edge(a, b, relation=rel)

print("Nodes:", g.number_of_nodes())
print("Edges:", g.number_of_edges())
print()
for a, b, data in g.edges(data=True):
    print(a, "--", data["relation"], "-->", b)


def get_properties(node):
    # go up the is_a / instance_of links and collect every "has" property
    props = []
    to_visit = [node]
    while len(to_visit) > 0:
        current = to_visit.pop()
        for _, nxt, data in g.out_edges(current, data=True):
            if data["relation"] == "has":
                props.append(nxt + " (from " + current + ")")
            elif data["relation"] in ("is_a", "instance_of"):
                to_visit.append(nxt)
    return props


print("\nProperties of Asha (inheritance):")
for p in get_properties("Asha"):
    print(" ", p)

# fixed positions so the graph is readable
pos = {
    "Person": (4, 5), "Name": (6.5, 5),
    "Student": (1.5, 3.5), "Professor": (6.5, 3.5),
    "Roll_No": (0, 5), "Employee_ID": (8, 5),
    "Asha": (0, 2), "Ravi": (2.5, 2), "Dr_Rao": (6.5, 2),
    "AI_Course": (4, 0.5), "CSE_Dept": (6.5, 0.5),
}

os.makedirs("outputs", exist_ok=True)
plt.figure(figsize=(13, 8))
nx.draw(g, pos, with_labels=True, node_color="lightblue", node_size=3600,
        font_size=9, edgecolors="black")
nx.draw_networkx_edge_labels(g, pos, edge_labels=nx.get_edge_attributes(g, "relation"),
                             font_size=8, font_color="darkred", label_pos=0.4)
plt.title("University Semantic Network")
plt.savefig("outputs/semantic_network.png", dpi=120, bbox_inches="tight")
print("\nSaved outputs/semantic_network.png")
```

## 3.4 Results / Output

```text
Nodes: 11
Edges: 13

Student -- is_a --> Person
Student -- has --> Roll_No
Person -- has --> Name
Professor -- is_a --> Person
Professor -- has --> Employee_ID
Asha -- instance_of --> Student
Asha -- enrolled_in --> AI_Course
Ravi -- instance_of --> Student
Ravi -- enrolled_in --> AI_Course
Dr_Rao -- instance_of --> Professor
Dr_Rao -- teaches --> AI_Course
Dr_Rao -- works_in --> CSE_Dept
AI_Course -- offered_by --> CSE_Dept

Properties of Asha (inheritance):
  Roll_No (from Student)
  Name (from Person)

Saved outputs/semantic_network.png
```

**Result:** the network has 11 nodes and 13 relations. Asking for the properties of `Asha` returns two properties, both inherited:

* `Roll_No` from `Student`
* `Name` from `Person`

`Employee_ID` is *not* returned for Asha, because it belongs to `Professor` and Asha is not connected to that class.

## 3.5 Performance Analysis

| Metric | Result |
|---|---|
| Accuracy / Precision / Recall / F1 / Confusion Matrix | Not Applicable (not a classification problem) |
| Nodes (concepts) | 11 |
| Edges (relations) | 13 |
| Relation types | 7 |
| Properties inherited by Asha | 2 (Roll_No, Name) |
| Time Complexity | O(E) to build, O(V + E) worst case for an inheritance lookup |
| Space Complexity | O(V + E) |

The network makes relationships visible and supports inheritance well. Its weakness is that it has no built-in way to express exceptions, defaults or rules.

## 3.6 Screenshots / Visualization

The generated diagram (saved by the program):

![Semantic Network](outputs/semantic_network.png)

Console screenshot:

![Console Output](outputs/Task3.png)

## 3.7 Learning Outcomes

* Modelled concepts and relationships as a labelled graph.
* Implemented property inheritance by traversing `is_a` and `instance_of` links.
* Used `networkx` and `matplotlib` to draw a hand-positioned hierarchy.
* Understood the difference between a class link (`is_a`) and an individual link (`instance_of`).

---

# 4. Frame Representation

## 4.1 Aim / Problem Statement

### Aim
To represent knowledge using **frames** (slot-and-value structures) with **inheritance**, default values that can be overridden, and a value computed from other slots.

### Problem Statement
Model a hierarchy `Person -> Student -> Asha / Ravi`. Each frame stores its own slots and inherits the rest from its parent. Compute whether a student is eligible for exams from their attendance.

### Example
```text
Person  : species = Human, can_speak = True
Student : role = Student, max_courses = 6   (is-a Person)
Asha    : roll_no, department, attendance = 82, courses   (is-a Student)
```

## 4.2 Algorithm

**Representation:** a `Frame` has a name, an optional parent frame and a dictionary of slots.

```text
Person  (species, can_speak)
   ▲
Student (role, max_courses)
   ▲                ▲
Asha (own slots)   Ravi (own slots)
```

**Slot lookup (inheritance):** look in the frame's own slots; if the slot is missing, ask the parent frame, and so on up the hierarchy.

**Computed slot:** `exam_status(student)` reads the `attendance` slot and returns `"Eligible for exams"` if attendance is at least 75, otherwise `"Attendance shortage"`.

### Pseudocode
```text
get(frame, slot):
    IF slot is in frame's own slots:
        RETURN its value
    IF frame has a parent:
        RETURN get(parent, slot)
    RETURN None

exam_status(student):
    IF get(student, "attendance") >= 75:
        RETURN "Eligible for exams"
    RETURN "Attendance shortage"
```

## 4.3 Implementation

```python
# Part 4: Frame Representation
# A frame is a set of slots (name: value). If a slot is missing,
# we look for it in the parent frame (inheritance).

class Frame:
    def __init__(self, name, parent=None, **slots):
        self.name = name
        self.parent = parent
        self.slots = slots

    def get(self, slot):
        if slot in self.slots:
            return self.slots[slot]
        if self.parent is not None:
            return self.parent.get(slot)
        return None

    def show(self):
        print("Frame:", self.name)
        # collect slot names from this frame and all parents
        names = []
        f = self
        while f is not None:
            for s in f.slots:
                if s not in names:
                    names.append(s)
            f = f.parent
        for s in names:
            where = "own" if s in self.slots else "inherited"
            print("  ", s, "=", self.get(s), "(" + where + ")")


def exam_status(student):
    # value is worked out from another slot when needed
    if student.get("attendance") >= 75:
        return "Eligible for exams"
    return "Attendance shortage"


person = Frame("Person", species="Human", can_speak=True)
student = Frame("Student", parent=person, role="Student", max_courses=6)
asha = Frame("Asha", parent=student, roll_no="CS101", department="CSE",
             attendance=82, courses=["AI", "DBMS"])
ravi = Frame("Ravi", parent=student, roll_no="CS102", department="CSE",
             attendance=68, courses=["AI"])

asha.show()
print("   exam status =", exam_status(asha))
print()
ravi.show()
print("   exam status =", exam_status(ravi))

print("\nInheritance check:")
print("Asha can_speak:", asha.get("can_speak"), "(from Person)")
print("Asha max_courses:", asha.get("max_courses"), "(from Student)")

print("\nOverriding a default:")
ravi.slots["max_courses"] = 4
print("Ravi max_courses:", ravi.get("max_courses"), "(own value)")
print("Asha max_courses:", asha.get("max_courses"), "(still default)")
```

## 4.4 Results / Output

```text
Frame: Asha
   roll_no = CS101 (own)
   department = CSE (own)
   attendance = 82 (own)
   courses = ['AI', 'DBMS'] (own)
   role = Student (inherited)
   max_courses = 6 (inherited)
   species = Human (inherited)
   can_speak = True (inherited)
   exam status = Eligible for exams

Frame: Ravi
   roll_no = CS102 (own)
   department = CSE (own)
   attendance = 68 (own)
   courses = ['AI'] (own)
   role = Student (inherited)
   max_courses = 6 (inherited)
   species = Human (inherited)
   can_speak = True (inherited)
   exam status = Attendance shortage

Inheritance check:
Asha can_speak: True (from Person)
Asha max_courses: 6 (from Student)

Overriding a default:
Ravi max_courses: 4 (own value)
Asha max_courses: 6 (still default)
```

**Result:**

| Slot | Asha | Ravi | Where it comes from |
|---|---|---|---|
| roll_no | CS101 | CS102 | own |
| attendance | 82 | 68 | own |
| role | Student | Student | inherited from Student |
| max_courses | 6 | 6 → 4 after override | default from Student, Ravi's override is his own |
| species, can_speak | Human, True | Human, True | inherited from Person |
| exam status | Eligible for exams | Attendance shortage | computed from attendance |

Changing Ravi's `max_courses` to 4 does not change Asha's value: the override is stored only in Ravi's frame, and Asha still reads the default from `Student`.

## 4.5 Performance Analysis

| Metric | Result |
|---|---|
| Accuracy / Precision / Recall / F1 / Confusion Matrix | Not Applicable (not a classification problem) |
| Frames | 4 (Person, Student, Asha, Ravi) |
| Slots stored | 2 (Person) + 2 (Student) + 4 (Asha) + 4 (Ravi) = 12 (13 after Ravi overrides max_courses) |
| Time Complexity | O(d) per slot lookup, d = depth of the hierarchy (3 here) |
| Space Complexity | O(total slots) |

The 75 % attendance threshold is an assumption chosen for the demo. Frames group everything known about one object in one place, which makes them easy to read, but they are weaker than rules at expressing "if this, then that" reasoning.

## 4.6 Screenshots / Visualization

```text
Frame: Asha  (is-a Student, is-a Person)
┌────────────────────────────────────────────┐
│ roll_no      CS101              own        │
│ department   CSE                own        │
│ attendance   82                 own        │
│ courses      [AI, DBMS]         own        │
│ role         Student            inherited  │
│ max_courses  6                  inherited  │
│ species      Human              inherited  │
│ can_speak    True               inherited  │
│ exam status  Eligible for exams computed   │
└────────────────────────────────────────────┘
```

Console screenshot:

![Console Output](outputs/Task4.png)

## 4.7 Learning Outcomes

* Built frames with slots, parents and inheritance.
* Saw how a child frame can override a default without affecting its siblings.
* Computed a slot value from other slots on demand.
* Compared the frame style with fact lists and graphs.

---

# 5. Logical Rule Engine (Forward Chaining)

## 5.1 Aim / Problem Statement

### Aim
To implement a **forward-chaining rule engine** that starts from known facts and repeatedly applies IF-THEN rules to derive new facts.

### Problem Statement
Given a set of facts and a list of rules of the form `IF condition1 AND condition2 THEN conclusion`, keep firing every rule whose conditions are all known until no new fact can be added. Demonstrate it on a medical rule set and a university rule set.

### Example
```text
Facts : fever, cough, body_ache
Rules : IF fever AND cough THEN suspect_flu
        IF suspect_flu AND body_ache THEN diagnosis_flu
        IF diagnosis_flu THEN advise_rest_and_fluids
```

## 5.2 Algorithm

**Representation:** a rule is a pair `([conditions], conclusion)`; the known facts are a list.

**Forward chaining:** repeat passes over all rules. In each pass, a rule fires if its conclusion is not yet known and all of its conditions are already known. The loop stops after a full pass that adds nothing.

### Pseudocode
```text
facts = starting facts
changed = True
WHILE changed:
    changed = False
    FOR EACH rule (conditions, conclusion):
        IF conclusion already in facts: skip
        IF every condition is in facts:
            add conclusion to facts
            record the rule as fired
            changed = True
RETURN facts and the list of fired rules
```

## 5.3 Implementation

```python
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
```

## 5.4 Results / Output

```text
--- Medical rules ---
Starting facts: ['fever', 'cough', 'body_ache']

Rules used:
  1. IF fever AND cough THEN suspect_flu
  2. IF suspect_flu AND body_ache THEN diagnosis_flu
  3. IF diagnosis_flu THEN advise_rest_and_fluids

New facts: ['suspect_flu', 'diagnosis_flu', 'advise_rest_and_fluids']

--- University rules ---
Starting facts: ['attendance_ok', 'assignments_done', 'passed_exam', 'credits_sufficient']

Rules used:
  1. IF attendance_ok AND assignments_done THEN eligible_for_exam
  2. IF eligible_for_exam AND passed_exam THEN course_completed
  3. IF course_completed AND credits_sufficient THEN eligible_for_graduation

New facts: ['eligible_for_exam', 'course_completed', 'eligible_for_graduation']
```

**Result:**

*Medical rules* (5 rules): from `fever, cough, body_ache` the engine fires 3 rules and derives `suspect_flu`, `diagnosis_flu` and `advise_rest_and_fluids`. The malaria rules did not fire because `chills` and `sweating` are not known.

*University rules* (3 rules): from `attendance_ok, assignments_done, passed_exam, credits_sufficient` the engine fires all 3 rules in a chain and derives `eligible_for_exam`, `course_completed` and `eligible_for_graduation`.

The program prints the rules that fired, in order, which explains *why* each conclusion was reached.

## 5.5 Performance Analysis

| Metric | Result |
|---|---|
| Accuracy / Precision / Recall / F1 / Confusion Matrix | Not Applicable (not a classification problem) |
| Medical rule set | 5 rules, 3 fired, 3 new facts |
| University rule set | 3 rules, 3 fired, 3 new facts |
| Passes over the rules | 2 for each set (the second pass only confirms that nothing changed) |
| Time Complexity | O(R^2 x C) rule checks in the worst case (up to R passes over R rules with C conditions each), each check being a list lookup |
| Space Complexity | O(F + R) for F facts and R rules |

Forward chaining is **data-driven**: it works forward from what is known and finds everything that follows. It is useful when you want all consequences of the facts; if you only want to prove one specific goal, backward chaining can be more efficient.

## 5.6 Screenshots / Visualization

```text
fever, cough ──R1──► suspect_flu
                         │
          body_ache ──R2─┴──► diagnosis_flu ──R3──► advise_rest_and_fluids

attendance_ok, assignments_done ──U1──► eligible_for_exam
                  passed_exam ──U2──► course_completed
             credits_sufficient ──U3──► eligible_for_graduation
```

Console screenshot:

![Console Output](outputs/Task5.png)

## 5.7 Learning Outcomes

* Wrote IF-THEN rules as data and applied them with a forward-chaining loop.
* Produced an explanation (the list of fired rules) for each conclusion.
* Saw how chained rules derive facts that were never stated directly.
* Understood the difference between forward and backward chaining.

---

# Analysis (Homework): Frames vs Semantic Networks vs Rule-Based Systems

All three representations were built in this lab for the same university domain, so they can be compared directly.

| Aspect | Semantic Network (Part 3) | Frames (Part 4) | Rule-Based System (Part 5) |
|---|---|---|---|
| Basic idea | Graph of concepts joined by labelled relations | Structured record of slots and values per object | IF-THEN rules over a set of facts |
| How the same fact looks | edge `Asha --instance_of--> Student` | frame `Asha` with slots `roll_no`, `attendance`, ... | fact `attendance_ok` used in rule conditions |
| Inheritance | Yes, along `is_a` / `instance_of` links | Yes, from the parent frame, with overriding defaults | No built-in inheritance |
| Reasoning | Traversing links | Looking up slots, running attached procedures | Chaining rules to derive new facts |
| Explains its answers | Shows the path of links | Shows which frame supplied a value | Shows the rules that fired |
| Strengths | Relationships are easy to see and draw | Everything about one object is in one place; defaults and overrides | Can express conditions and decisions; derives new knowledge |
| Weaknesses | Hard to express rules, exceptions or procedures | Weak at multi-step logical reasoning | Many rules become hard to manage; no structure for objects |
| Best suited for | Showing how concepts relate | Describing objects and their attributes | Decision making and expert systems |

### When to use which

* **Semantic network:** when the main question is *how things are related* (for example, which course a professor teaches, or what a student inherits from `Person`).
* **Frames:** when you need a complete description of each object with sensible defaults (for example, a student record with a default course limit that one student overrides).
* **Rules:** when you need to *decide or conclude* something from facts (for example, deciding exam eligibility or suggesting an action).

### Observation

None of the three is best on its own. Real knowledge-based systems combine them: frames or networks to describe the domain, and rules to reason about it. The predicate facts of Part 1 are a fourth view: they are flexible and easy to query, but they offer no structure or inheritance by themselves.

---

# Conclusion

Five small programs represent the same kind of knowledge in different ways: predicate facts for direct queries, a structured medical knowledge base with a matching score, a semantic network with inheritance, frames with slots and defaults, and a forward-chaining rule engine that derives new facts and explains how. Comparing them shows that each representation is good at a different job: networks for relationships, frames for objects, and rules for decisions.