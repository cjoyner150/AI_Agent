from functions.write_file import write_file


def main():
    display_file_write_result("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    display_file_write_result("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    display_file_write_result("calculator", "/tmp/temp.txt", "this should not be allowed")

def display_file_write_result(working_dir:str, dir: str, content: str) -> None:
    result = write_file(working_dir, dir, content)

    print(f"\n=================== Results for {dir} ===================\n")
    print(f"{dir} result: {result}\n")

main()
