import basic

while True:
    text = input('basic> ')
    result, error = basic.run('<stdin>', text)

    if text == "break": break
    print(text)

    if error: print(error.as_string())
    else: print(result)