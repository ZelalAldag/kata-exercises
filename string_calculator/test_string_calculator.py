import pytest
from string_calculator import StringCalculator


class TestStringCalculator:
    @pytest.fixture(autouse=True)
    def _init_tests(self):
        self.string_calculator = StringCalculator()

    @pytest.mark.parametrize(
        "input_val,expected_val",
        [("", 0), ("1", 1), ("1,2", 3), ("12,13", 25)],
    )
    def test_add_basics(self, input_val, expected_val):
        result = self.string_calculator.add(input_val)
        assert isinstance(result, int)
        assert result == expected_val

    @pytest.mark.parametrize(
        "input_val,expected_val",
        [("1,2,3", 6), ("12,1,1,1,1", 16)],
    )
    def test_add_unknown_number_of_param(self, input_val, expected_val):
        result = self.string_calculator.add(input_val)
        assert result == expected_val

    def test_add_new_line(self):
        result = self.string_calculator.add("1\n2,3")
        assert result == 6

    def test_add_new_line_multiple(self):
        result = self.string_calculator.add("1\n2,3\n4\n4,1")
        assert result == 15

    def test_add_different_delimeters(self):
        result = self.string_calculator.add("//;\n1;2")
        assert result == 3

    def test_add_different_delimeters_multiple_comma(self):
        result = self.string_calculator.add("//,\n1,2,3")
        assert result == 6

    def test_add_negative(self):
        with pytest.raises(ValueError) as error:
            self.string_calculator.add("1,2,-3")

        assert "negatives not allowed" in str(error.value)
        assert "-3" in str(error.value)

    def test_add_negative_delimeter(self):
        result = self.string_calculator.add("//-\n1-2-3")
        assert result == 6

    def test_add_negative_delimeter_error(self):
        with pytest.raises(ValueError) as error:
            self.string_calculator.add("//-\n1-2--3")

        assert "negatives not allowed" in str(error.value)
        assert "-3" in str(error.value)

    def test_add_multiple_negative_error(self):
        with pytest.raises(ValueError) as error:
            self.string_calculator.add("1,2,-3,-4,-5")

        assert "negatives not allowed" in str(error.value)
        assert ("-3" and "-4" and "-5") in str(error.value)
        assert ("1" and "2") not in str(error.value)

    def test_add_multiple_delimeter_negative_error(self):
        with pytest.raises(ValueError) as error:
            self.string_calculator.add("//-\n1--2--3--4--5")

        assert "negatives not allowed" in str(error.value)
        assert ("-2" and "-3" and "-4" and "-5") in str(error.value)
        assert ("1") not in str(error.value)

    def test_add_multiple_delimeter_all_negative_error(self):
        with pytest.raises(ValueError) as error:
            self.string_calculator.add("//-\n-1--2--3")

        assert "negatives not allowed" in str(error.value)
        assert ("-1" and "-2" and "-3") in str(error.value)

    def test_get_called_count(self):
        self.string_calculator.add("1\n2,3")
        self.string_calculator.add("1,2,3")
        self.string_calculator.add("//*\n1*2*3")

        result = vars(self.string_calculator)
        assert result["called_count"] == 3

    def test_add_bigger_1000(self):
        result = self.string_calculator.add("1,2,1001")
        assert result == 3

    def test_add_with_1000(self):
        result = self.string_calculator.add("1,2,1000")
        assert result == 1003

    def test_add_long_delimeter(self):
        result = self.string_calculator.add("//[***]\n1***2***3")
        assert result == 6

    def test_add_long_delimeter_single(self):
        result = self.string_calculator.add("//[*]\n1*2*3")
        assert result == 6

    def test_add_long_delimeter_negative(self):
        with pytest.raises(ValueError) as error:
            self.string_calculator.add("//[***]\n-1***-2***3")

        assert "negatives not allowed" in str(error.value)
        assert ("-1" and "-2") in str(error.value)

    def test_multiple_delimeter_custom(self):
        result = self.string_calculator.add("//[*][%]\n1*2%3")
        assert result == 6

    def test_long_multiple_delimeter(self):
        result = self.string_calculator.add("//[**][%%]\n1**2%%3")
        assert result == 6

    def test_long_and_short_multiple_delimeter(self):
        result = self.string_calculator.add("//[**][%%][*]\n1**2%%3*4")
        assert result == 10
