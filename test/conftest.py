from pytest import fixture


def pytest_addoption(parser):
    parser.addoption("--args", action="store",default = "")

@fixture()
def args(request):
    args = request.config.getoption("--args")
    if args:
        print(f"received {args=}")
    return args