from interpreterv3 import Interpreter


def main():
    interpreter = Interpreter()
    program1 = """
        func main() {
        x = lambda(ref f, ref g) {
            print(f == g);
            print(a == b);
            f = g;
            print(f == g);
            print(a == b);
        };
        a = 5;
        b = 10;
        x(a, b);
        print(a == b);

        /*
        *OUT*
        false
        false
        true
        true
        true
        *OUT*
        */
        }

    """
    interpreter.run(program1)
    print("Program done.")

if __name__ == "__main__":
    main()