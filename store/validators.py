from django.core.exceptions import ValidationError

# creating a validator function
def validate_file_size(file):
    # in here < file > is an instance of the field we are using the validator for
    # example --> in this project field=models.ImageField --> which has an attribute < size >
    max_size_kb = 50

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_kb}KB!')
