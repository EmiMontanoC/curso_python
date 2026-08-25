class Athlete:
    ''' A class to represent an athlete.'''
    def __init__(self, name, age, sport):
        self.name = name
        self.age = age
        self.sport = sport
    
    def __str__(self):
        return f"Athlete(name={self.name}, age={self.age}, sport={self.sport})"
    
    def __repr__(self):
        return f"Athlete(name='{self.name}', age={self.age}, sport='{self.sport}')"
    
    def display(self):
        print(f"|{self.name} | {self.age} | {self.sport} |")
        
    
    
def main():
    ''' Test the class '''
    a = Athlete("Ana G",25,"200m")
    b = Athlete("John D",30,"100m")
    print(a)
    print(b)
    print(repr(a))
    print(repr(b))
    a.display()
    b.display()
    c = eval(repr(b))
    print(c)
    print(f"c is b: {c is b}")
    print(f"id c:{id(c)}, id b: {id(b)}")

if __name__ == "__main__":
    main()