def water_jug(x, y, target):
    a = 0
    b = 0

    while a != target and b != target:

        # If first jug is empty, fill it
        if a == 0:
            a = x
            print(f"Fill {x}L jug")

        # If second jug is full, empty it
        elif b == y:
            b = 0
            print(f"Empty {y}L jug")

        # Pour first jug into second jug
        else:
            amount = min(a, y - b)

            a = a - amount
            b = b + amount

            print(f"Pour {x}L -> {y}L")

        print(f"State: ({a}, {b})")
        print()

    print("Target reached!")


water_jug(5, 7, 4)