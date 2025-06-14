from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
model=OllamaLLM(model="llama3.2")

def check(Question):
    template="""

    Determine whether the given question belongs to one of the following branches of mathematics:  
    Algebra, Probability, Precalculus, Prealgebra, Number Theory, Geometry, Intermediate Algebra.  

    - If the question is mathematical, return "yes"  
    - If it is related to programming, general topics, or other subjects, return "no"  
    - only return yes or no

    Question: {question}  
    Answer:

    
        """

    prompt=ChatPromptTemplate.from_template(template)
    chain= prompt | model 


    result=chain.invoke({"question":Question})
    return result

