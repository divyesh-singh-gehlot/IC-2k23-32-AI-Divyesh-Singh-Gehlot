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