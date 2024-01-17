
class FileHandler:
    def __init__(self):
        pass

    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ""
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def display_text(self, file_path):
        file_content = self.read_file(file_path)

        if not file_content:
            print(f"File not found at path: {file_path}")
        else:
            print(file_content)
