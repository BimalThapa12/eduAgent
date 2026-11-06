
# EduAgent AI - Generation Strategies

GENERATION_STRATEGIES = {

    "S1": {
        "name": "Simple First",
        "description": "Explain concepts using very simple English.",
        "instructions": """
        Use simple English and short sentences.
        Assume the learner has zero technical knowledge.
        Explain every technical term immediately.
        Avoid complicated vocabulary.
        """
    },

    "S2": {
        "name": "Example First",
        "description": "Teach concepts through relatable examples.",
        "instructions": """
        Start by introducing a relatable real-world example.
        Explain the technical concept using that example.
        Use examples from everyday life.
        Connect each concept to practical situations.
        """
    },

    "S3": {
        "name": "Step By Step",
        "description": "Teach concepts in a logical sequence.",
        "instructions": """
        Divide the lesson into small learning steps.
        Explain one concept before moving to the next.
        Use numbered explanations.
        Build knowledge gradually.
        """
    },

    "S4": {
        "name": "Analogy Based",
        "description": "Use everyday comparisons to explain concepts.",
        "instructions": """
        Use simple everyday analogies.
        Compare technical concepts with familiar situations.
        Explain where the analogy is useful and where it differs.
        Keep explanations beginner-friendly.
        """
    },

    "S5": {
        "name": "Hybrid Learning",
        "description": "Combine simple language, examples and analogies.",
        "instructions": """
        Use simple English.
        Introduce relatable examples.
        Explain technical terms.
        Use everyday analogies where helpful.
        Teach concepts step by step.
        Combine all these approaches into one coherent lesson.
        """
    }

}


def get_strategy(strategy_id):

    return GENERATION_STRATEGIES.get(strategy_id)


def get_all_strategies():

    return GENERATION_STRATEGIES
