class FileReader:
    def __init__(self, file_name: str):
        self._file = open(file_name)

    def __iter__(self):
        for line in self._file:
            yield line.strip()
