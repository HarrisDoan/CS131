from interpreterv4 import Interpreter


def main():
    interpreter = Interpreter()
    program1 = """

    func main() {
        a = @;
        a.x = 5;

        print(a.x);
    }

    """
    interpreter.run(program1)
    print("Program done.")

if __name__ == "__main__":
    main()