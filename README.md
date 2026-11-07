# EduAgent AI – Self-Evaluating Lesson Content Generator
## Complete Project Demonstration Script

### 1. Introduction and Project Overview

Hello everyone.

Today, I am going to present my project, **EduAgent AI – Self-Evaluating Lesson Content Generator**.

The main objective of this project is to develop an AI-powered educational content generation system that does more than simply generate lessons.

Most traditional AI applications take a prompt from the user, generate an answer, and return that answer. However, they do not necessarily verify whether the generated content is technically accurate, easy to understand, complete, or suitable for the target audience.

This is the problem I wanted to address through EduAgent AI.

I designed this system to generate educational lessons, evaluate their quality, identify mistakes, and automatically improve the content using feedback.

For this demonstration, I am using the topic **Introduction to Retrieval-Augmented Generation, also known as RAG**.

The target audience is a student who has completed their 12th grade and has limited English vocabulary.

The system should explain technical concepts using simple language, familiar examples, and a clear teaching structure.

The important part is that the system should not approve a lesson simply because an AI model has generated it. It must first pass predefined quality requirements.

### 2. Technology Stack

Before explaining the workflow, let me briefly introduce the technologies I used.

The main programming language is Python.

For the language model, I integrated Ollama with the Llama 3.2 3B model. I chose Ollama because it allows me to run the model locally instead of depending entirely on external API services.

For workflow orchestration, I used LangGraph.

LangGraph allows me to connect multiple agents into a structured workflow, manage the state between agents, and control conditional execution.

For persistent memory, I used SQLite.

SQLite stores historical strategy performance and reward information so that the system can use previous execution results when selecting future generation strategies.

I also implemented structured JSON evaluation outputs, Markdown lesson generation, and readable text-based workflow logs.

### 3. Project Architecture and Folder Structure

Now let me explain how the project is organized.

The project follows a modular, multi-agent architecture.

Inside the project, I have separated the agents, workflow, memory, knowledge, prompts, reinforcement learning components, and utility functions into different folders.

The agents folder contains the main AI components.

The workflow folder contains the LangGraph state definition and graph implementation.

The memory folder contains the SQLite database and memory management logic.

The knowledge folder contains the reference material used to ground the generated lesson.

The prompts folder contains separate instructions for generation, evaluation, and improvement.

The reinforcement folder contains the generation strategies, reward calculation, strategy selection, and policy management components.

Finally, the outputs folder stores approved lessons and structured evaluation results, while the logs folder stores readable execution logs.

This modular structure makes the system easier to maintain, test, and extend.

### 4. Topic Analyzer and Reference Material

Now I will explain how the system understands the topic before generating the lesson.

I created a Topic Analyzer agent.

Its responsibility is to analyze the requested topic and identify the essential concepts that must be included in the final lesson.

For this demonstration, the topic is Introduction to RAG.

The Topic Analyzer identifies five essential learning areas.

First, the definition of Retrieval-Augmented Generation.

Second, the two main components, retrieval and generation.

Third, the complete RAG workflow.

Fourth, the difference between RAG and a traditional Large Language Model.

And finally, the benefits and limitations of RAG.

I also created a reference document inside the knowledge folder.

This document acts as the source material for the lesson.

The Generator uses this reference material to create content, while the Evaluator checks whether the generated lesson is grounded in the supplied information.

This is important because I do not want the system to generate explanations that are unrelated to the reference material.

I also implemented a Topic Validator.

It checks whether the generated lesson correctly covers the intended topic and prevents incorrect interpretations, such as confusing Retrieval-Augmented Generation with Risk Assessment Grid.

### 5. Lesson Generator and Ollama Integration

Next is the Generator agent.

The Generator is responsible for creating the actual educational lesson.

It receives the topic, student level, selected generation strategy, reference material, and topic requirements.

Using this information, it creates a complete lesson with sections such as:

- Introduction to the topic.
- Definition.
- How the technology works.
- Important concepts.
- Practical examples.
- Benefits and limitations.
- Summary.
- Knowledge-check questions.

One feature I implemented here is live streaming through Ollama.

Instead of waiting until the entire lesson has been generated, the generated content appears progressively in the terminal.

This makes the generation process visible during execution.

I also created a separate regeneration function.

This function receives the previous lesson and the improvement instructions from the Improvement Agent.

Therefore, when a lesson fails evaluation, the system can regenerate the content using the feedback rather than treating every attempt as a completely unrelated generation.

### 6. Evaluator and the R1–R8 Quality Rubric

Now comes one of the most important components of EduAgent: the Evaluator.

I did not want to depend on a simple response such as whether the lesson looks good or bad.

Instead, I created eight predefined quality requirements.

These are R1 to R8.

R1 is Technical Accuracy. It checks whether the technical explanations are correct.

R2 is Grounding in Reference Material. It checks whether the lesson follows the supplied source material.

R3 is Beginner Friendliness. It checks whether the lesson is suitable for someone with limited technical knowledge.

R4 is Simple Language. It checks whether the explanations use understandable vocabulary and sentence structures.

R5 is Practical Examples. It checks whether the lesson contains relevant real-world examples.

R6 is Topic Coverage. It checks whether the essential learning concepts are included.

R7 is Teaching Flow. It checks whether the lesson follows a logical sequence.

R8 is Standalone Quality. It checks whether a student can understand the lesson without needing additional external explanations.

Each criterion returns either PASS or FAIL, along with supporting evidence and feedback.

I also implemented validation for the evaluator's response.

For example, if the evaluator returns generic evidence or does not provide sufficient information, the system does not blindly accept that result.

The evaluation result is processed and checked before the final approval decision.

Most importantly, the lesson is approved only when all eight criteria pass and the topic validation also succeeds.

This keeps the quality requirements separate from the generation process.

### 7. Improvement Agent and Self-Evaluation Loop

Now I will explain how the system learns from mistakes during the same execution.

Suppose the Generator creates a lesson, but the Evaluator identifies problems.

For example, the lesson may contain complicated English or an incomplete technical explanation.

The Evaluator marks the relevant criteria as FAIL and provides feedback.

The Improvement Agent receives this evaluation result.

Its responsibility is to convert the evaluator's feedback into clear instructions that the Generator can understand.

For example, it may instruct the Generator to use simpler language, explain technical terms more clearly, or include additional examples.

The system then sends the previous lesson, the evaluation feedback, and the improvement instructions back to the Generator.

The Generator creates a revised version.

After regeneration, the Evaluator checks the new lesson again using the same quality rubric.

This process continues until the lesson passes or the maximum retry limit is reached.

In my current configuration, the maximum retry count is two.

That means the system can perform one initial generation and up to two additional regeneration attempts.

This is the feedback-driven self-improvement mechanism of EduAgent.

### 8. Reinforcement Learning and Strategy Selection

Another important component is the reinforcement-based strategy selection mechanism.

I wanted the system to use historical performance rather than always selecting a generation strategy randomly.

For this, I implemented a UCB-based strategy selection approach, which stands for Upper Confidence Bound.

The idea is to balance two things: exploration and exploitation.

Exploration means trying strategies that have not been used frequently, so the system can discover whether they perform well.

Exploitation means selecting strategies that have already demonstrated good performance.

The strategy selector considers previous performance and the number of times each strategy has been used.

After a workflow finishes, the system calculates a reward based on the final evaluation result.

The reward is then used to update the selected strategy's historical performance.

An important implementation detail is that the same strategy is retained during retries within a single workflow run.

This helps make the reward attribution fair because the system is evaluating the outcome of one selected strategy rather than switching strategies halfway through the process.

The system updates the reward once after the final workflow outcome.

This is not neural network training or Llama fine-tuning. It is a bandit-based learning mechanism that improves future strategy selection using historical feedback.

### 9. SQLite Memory and Persistent Learning

Now let me explain the memory component.

I used SQLite to maintain persistent information across different executions.

The purpose of this memory is to ensure that the system does not treat every execution as completely independent.

The database stores information related to strategy performance and historical reward updates.

When a new workflow starts, the strategy selection mechanism can use this historical information to make a better decision.

For example, if a particular strategy has consistently performed well, it may receive a higher selection preference.

However, the UCB algorithm still allows exploration of other strategies.

This creates a feedback loop across multiple executions.

The system generates content, evaluates the result, calculates the reward, stores the result, and uses historical performance in future strategy selection.

That is how EduAgent implements persistent, feedback-based workflow learning.

### 10. Live Project Demonstration

Now I will demonstrate the actual implementation.

I am opening the project in Visual Studio Code.

Here is the project structure and the different modules I explained earlier.

I have already configured Ollama with the Llama 3.2 3B model.

The reference material is available in the knowledge folder, and the quality rubric is defined in the Evaluator.

Now I will run the application.

[Run the application]

```bash
python3 main.py
```

The workflow starts by selecting a generation strategy.

Next, the Topic Analyzer analyzes the Introduction to RAG topic and identifies the essential learning concepts.

The Generator then starts creating the lesson.

You can see that the generated lesson appears progressively in the terminal through Ollama streaming.

After generation, the Topic Validator checks whether the lesson correctly matches the requested topic.

Next, the Evaluator checks the lesson against all eight quality requirements.

[If a criterion fails, point to the failed result.]

Here, you can see that the Evaluator has identified a failed criterion.

The system does not immediately approve the lesson.

Instead, it sends the feedback to the Improvement Agent.

The Improvement Agent prepares instructions, and the Generator receives those instructions along with the previous lesson.

The second attempt begins.

[Show the regeneration output if the run triggers it.]

After regeneration, the Evaluator checks the lesson again.

If all eight criteria pass and topic validation succeeds, the system approves the lesson.

Otherwise, it continues within the retry limit and eventually rejects the lesson if it still fails.

Finally, the system calculates the reward and updates the strategy performance.

### 11. Generated Outputs and Logs

After the workflow completes, I can show the generated files.

The approved lesson is saved in Markdown format inside the outputs/lessons folder.

The evaluation result is saved separately as a JSON file inside outputs/evaluation_logs.

The readable execution log is saved in the logs folder.

The SQLite database maintains the persistent strategy and reward information.

This separation makes it easier to inspect the final lesson, understand why it was approved or rejected, and review the workflow execution.

### 12. Current Limitations and Future Improvements

There are some limitations in the current implementation.

First, I am using a relatively small local model, Llama 3.2 3B, because the project is running on local hardware.

Second, LLM-based evaluation cannot guarantee factual correctness. Stronger factual verification can be added in future versions.

Third, the current Topic Validator uses keyword-based coverage checks, so semantic validation can be improved.

Fourth, the current implementation is specifically tailored to the Introduction to RAG assessment.

I also plan to develop a Streamlit interface so users can interact with EduAgent through a web-based interface instead of running everything through the terminal.

Other improvements include stronger evidence validation, more automated tests, better semantic topic validation, and additional generation strategies.

### 13. Conclusion

To conclude, EduAgent AI is designed to go beyond ordinary AI content generation.

It combines multiple agents, reference-grounded generation, structured evaluation, feedback-driven regeneration, persistent memory, and UCB-based strategy selection.

The main idea behind this project is simple:

Generating content is not enough. The system should also evaluate the content, identify mistakes, improve the result, and maintain a record of its performance.

Through EduAgent, I have implemented a workflow that brings these capabilities together using Python, LangGraph, Ollama, and SQLite.

Thank you for watching my demonstration.