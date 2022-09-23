class Research:
    def file_reader(self) -> str:
        with open('data.csv', 'r', encoding='utf-8') as file:
            return file.read()

if __name__ == '__main__':
    r = Research()
    print(r.file_reader())
