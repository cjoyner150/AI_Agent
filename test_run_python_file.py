from functions.run_python_file import run_python_file


def main():
    display_file_run_result("calculator", "main.py")
    display_file_run_result("calculator", "main.py", ["3 + 5"])
    display_file_run_result("calculator", "tests.py")
    display_file_run_result("calculator", "../main.py")
    display_file_run_result("calculator", "nonexistent.py")
    display_file_run_result("calculator", "lorem.txt")

def display_file_run_result(working_dir:str, dir: str, args: list[str] | None = None) -> None:
    result = run_python_file(working_dir, dir, args)

    print(f"\n=================== Results for {dir} ===================\n")
    print(f"{dir} result: {result}\n")

main()
