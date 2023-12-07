from interpreterv2 import Interpreter


def main():
    interpreter = Interpreter()
    program1 = """

    func main() {
        a = true;
        b = !true;
        c = 1;
        d = -c;
        print(a);
        print(b);
        print(c);
        print(d);
    }

/*
*OUT*
true
false
1
-1
*OUT*
*/
    """
    interpreter.run(program1)
    print("Program done.")

if __name__ == "__main__":
    main()