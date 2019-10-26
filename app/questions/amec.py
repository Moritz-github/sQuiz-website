import random

units = {
    "P": "Watt",
    "I": "Ampere",
    "U": "Volt",
    "R": "Ohm"
}

def question_calculateWiederstand():
    random1 = random.randint(1,10)
    random2 = random.randint(1,10)

    # Rechnet das ergebnis aus, und rundet es auf 2 nachkommastellen
    result = (random1*random2)/(random1+random2)
    answer = "{:.2f}".format(result)

    question = "Rechne: Was ist der gesamtwiederstand von {} und {} in einer Parallelschaltung? \
        (2 Nachkommastellen, gerundet)".format(random1, random2)


    return [question, answer]

def question_namenFormel():
    random_shortened_unit = list(units.keys())[random.randint(0, len(units)-1)]
    answer = units[random_shortened_unit]
    
    question = "Was ist die Einheit von {}?".format(random_shortened_unit)


    return [question, answer]

amec_functions = {
    question_namenFormel,
    question_calculateWiederstand
}