from functions.get_files_info import get_files_info

test_string_1 = "Result for current directory: "
test_string_2 = "Result for 'pkg' directory: "
test_string_3 = "Result for '/bin' directory: "
test_string_4 = "Result for '../' directory: "

working_dir = "calculator"

test_string_1 += f"\n{get_files_info(working_dir, ".")}"
print(test_string_1)

test_string_2 += f"\n{get_files_info(working_dir, "pkg")}"
print(test_string_2)

test_string_3 += f"\n{get_files_info(working_dir, "/bin")}"
print(test_string_3)

test_string_4 += f"\n{get_files_info(working_dir, "../")}"
print(test_string_4)