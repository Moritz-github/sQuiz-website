from app.questions.pool import question_pool
from app.questions.chemistry import chemistry_question
from app.questions.amec import amec_functions

pool_chemistry = question_pool(chemistry_question, "Chemie")

pool_amec = question_pool(amec_functions, "AMec")

question_pools = {"Amec": pool_amec, "Chemie": pool_chemistry}