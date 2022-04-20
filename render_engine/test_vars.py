class TestClass:
    foo = 'bar'

    def __init__(self):
        self.bar = 'biz'


test = TestClass()
test.biz = "bash"
print(f"{vars(test)=}")
print(f"{test.__dict__=}")

