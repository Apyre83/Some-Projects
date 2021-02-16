class Test():
    def __init__(self, pseudo, age):
        self.pseudo = pseudo
        self.age = age

    def __repr__(self):
        return str("test")

print(Test("1", 12))
