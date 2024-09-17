import pytest

@pytest.fixture(autouse=True)
def setup_helpers(request):
    def info(message):
        print(f"\n[INFO] {message}")

    def error(message):
        print(f"\n[ERROR] {message}")

    request.node.helpers = type('Helpers', (), {'info': info, 'error': error})
    pytest.helpers = request.node.helpers