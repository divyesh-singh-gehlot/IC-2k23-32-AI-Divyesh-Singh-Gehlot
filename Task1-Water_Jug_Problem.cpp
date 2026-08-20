#include <iostream>
using namespace std;

void waterJug(int x, int y, int target) {
    int a = 0, b = 0;

    while (a != target && b != target) {
        // If first jug is empty, fill it
        if (a == 0) {
            a = x;
            cout << "Fill " << x << "L jug";
        }

        // If second jug is full, empty it
        else if (b == y) {
            b = 0;
            cout << "Empty " << y << "L jug";
        }

        // Pour first jug into second jug
        else {
            int amount = min(a, y - b);

            a = a - amount;
            b = b + amount;

            cout << "Pour " << x << "L -> " << y << "L\n";
        }

        cout << "State: (" << a << ", " << b << ")\n\n";
    }

    cout << "Target reached!";
}

int main() {
    waterJug(5, 7, 4);

    return 0;
}