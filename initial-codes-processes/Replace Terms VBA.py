import openpyxl

def multi_find_replace():
    input_range_address = input("Original Range: ")
    replace_range_address = input("Replace Range: ")

    workbook = openpyxl.load_workbook("your_file.xlsx")
    input_range = workbook.active[input_range_address]
    replace_range = workbook.active[replace_range_address]

    for rng in replace_range.columns[0]:
        input_range = input_range.replace(rng.value, rng.offset(0, 1).value)

    workbook.save("your_file.xlsx")

multi_find_replace()
