from functions.write_file import write_file

result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print("test_one")
print(result)

result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print("test_two")
print(result)

result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print("test_three")
print(result)