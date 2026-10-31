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