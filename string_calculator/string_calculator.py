import re


class StringCalculator:
    def __init__(self):
        self.called_count = 0

    def add(self, numbers: str) -> int:
        self.get_called_count()
        if numbers == "":
            return 0

        multiple_delim = False
        err_result = []
        if numbers[:2] == "//":
            parts = numbers.partition("\n")
            delim = re.split(r"\[|\]", parts[0][2:])

            for i in delim:
                if len(i) > 1:
                    multiple_delim = True
            delim = [i for i in delim if i != ""]
            numbers = parts[2]
        else:
            delim = ["\n", ","]

        if multiple_delim:
            result = re.split("(?<=\\d)" + "\\" + "\\".join(delim[0]), numbers)
        else:
            result = re.split(
                "(?<=\\d)" + "[" + "|".join(delim) + "]", numbers
            )

        err_result = [i for i in result if "-" in i]
        if err_result != []:
            raise ValueError(
                "negatives not allowed: %s" % " ".join(err_result)
            )

        return sum([int(i) for i in result if int(i) <= 1000])

    def get_called_count(self):
        self.called_count += 1
