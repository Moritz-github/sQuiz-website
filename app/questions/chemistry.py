import random

dict_komplexionen = {"Sulfit":"SO3 2-",
                     "Sulfat":"SO4 2-",
                     "Nitrit":"NO2 1-",
                     "Nitrat":"NO3 1-",
                     "Carbonat":"CO3 2-",
                     "Phosphat":"PO4 3-",
                     "Silicat":"SiO3 2-",
                     "Hydroxid":"OH 1-",
                     "Ammonium":"NH4 1+"}

def chemistry_question():
    name = list(dict_komplexionen.keys())[random.randint(0, len(dict_komplexionen)-1)]
    formula = dict_komplexionen[name]
    question = ""
    if random.randint(0,1) == 0:
        question = "Was ist die Formel von {}: ".format(name)
        return [question, formula]        
    else:
        question = "Was ist der Name von {}: ".format(formula)
        return [question, name]
    