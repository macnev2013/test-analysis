from .models import TestResults

def get_test_key(test_results: TestResults):
    return f"{test_results.test_file_name}:{test_results.test_name}"
