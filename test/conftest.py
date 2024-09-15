from pytest import fixture

def pytest_addoption(parser):
    parser.addoption("--args", action="store",default = "")

@fixture()
def args(request):
    return request.config.getoption("--args")