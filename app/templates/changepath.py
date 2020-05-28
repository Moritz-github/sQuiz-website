import os
for filename in os.listdir():
    if os.path.splitext(filename)[1] == ".html":
        print(filename)
        with open(filename, "r+") as file:
            filetext = file.read()
            filetext = filetext.replace('href="assets/', 'href="/static/assets/')
            filetext = filetext.replace('src="assets/', 'src="/static/assets/')
            filetext = filetext.replace('<title>index</title>', '')
            file.seek(0)
            file.write(filetext)
            file.truncate()
