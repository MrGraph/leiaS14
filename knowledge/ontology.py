from semantics.concept import Concept
from semantics.slot import Slot


"We agreed with Kyle that class declarations shall represent concepts while a class instance corresponds to a concept instance"
class Animal(Concept):
    pass


class Fish(Animal):
    pass


class Buy(Concept):
    theme = Slot(Animal)
 
    
class Event(Concept):
    theme = Slot(Fish)
    agent = Slot(Animal)

    
class BuyEvent(Event):
    pass


class FishEvent(Event):
    theme = Slot(Fish)
    
    
class QuestionEvent(Event):
    pass