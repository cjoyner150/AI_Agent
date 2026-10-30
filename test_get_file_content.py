from functions.get_file_content import get_file_content

def main():
    display_file_content_result("calculator", "lorem.txt")
    display_file_content_result("calculator", "main.py")
    display_file_content_result("calculator", "pkg/calculator.py")
    display_file_content_result("calculator", "/bin/cat")
    display_file_content_result("calculator", "pkg/does_not_exist.py")

def display_file_content_result(working_dir:str, dir: str) -> None:
    result = get_file_content(working_dir, dir)
    truncated: bool = 'truncated' in result

    print(f"\n=================== Results for {dir} ===================\n")

    if (not truncated):
        print(f"{dir} result: {result}")

    print(f"{dir} length: {len(result)}")
    print(f"{dir} truncated: {truncated}\n")

main()
