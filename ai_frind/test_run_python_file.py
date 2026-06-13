from functions.run_python_file import run_python_file

result = run_python_file("calculator", "main.py")
print("test 1")
print(result)

result = run_python_file("calculator", "main.py", ["3 + 5"])
print("test 2")
print(result)

result = run_python_file("calculator", "tests.py")
print("test 3")
print(result)

result = run_python_file("calculator", "../main.py")
print("test 4")
print(result)

result = run_python_file("calculator", "nonexistent.py")
print("test 5")
print(result)

result = run_python_file("calculator", "lorem.txt")
print("test 6")
print(result)
