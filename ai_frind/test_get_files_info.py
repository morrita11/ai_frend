from functions.get_files_info import get_files_info

def test():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)

    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.tex truncated: {"truncated" in result}")

    result = get_file_content("calculater", "main.py")
    print(f"main.py length:{len(result)}")
    print(f"main.pytruncated: {"truncated" in result}")

if __name__ == "__main__":
    test()
