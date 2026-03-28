# Day 1 Learnings

Day 1 was about loading the data - specifically the documentation files from a Github repo that you want to interact with.

A couple of new things I was introduced to 
1. The `uv` python library - it's package manager like poetry
2. Frontmatter in markdown files
    - What if you could store the metadata of the markdown files, within the markdown file itself
    - Well that's basically what the Frontmatter format offers
    - How's it useful: Say for instance you are scanning your documentation and are looking for docs related to "XYZ" -> with frontmatter formating you don't need to go through the markdown content, you can simply check the metadata. Super helpful for language models, it could help save resources.

I have a couple repositories in mind that I could use for my project, but I think I'll use one of my own
https://github.com/Joyan9/learning_data_engineering -> In this repo, I have stored a lot of topics related to analytics engineering.
    
# Day 2 Learnings

Day 2 was about splitting the documents into manageable parts - also called as chunking. This is done so that
1. avoid excessive costs when using a LLM
2. to skip irrelevant content
3. improve the overall performance

It reminds me of the concept of partitioning - where we split a large dataset into smaller chunks, making it easier for lookups and computation.

There were 3 methods shown for chunking
1. sliding window chunking / character based chunking
    - This one was fairly simple, you split the document on regular interval based on the character count.
    - However what differentiates sliding window chunking is that the chunks have overlaps - why? Because to reduce context loss. Like if you are reading a book and the chapter ends abruptly 
2. Splitting by paragraphs or sections
    - As the name suggests, we split by sections and paragraphs
    - This method succeeds when the documentation is well-structured


3. Splitting by a LLM
    - finally the big boss method, this method is certainly not free as it requires an LLM to process large amounts text
    - Useful when the documentation is not structured, or you require the chunks to be coherent


So how should we decided which method to use, or perhaps a combination?
- As such there is not set rule, but as a rule of thumb start with the low-effort approach and if that provides good enough results then we don't need to add any more complexity
- Move towards the complex methods only if the performance justifies the effort.

As part of my homework we were supposed to try out each of the chunking methods on our own project and evaluate (roughly) which method works best for me. In my case it seems like the splitting by sections and paragraph works the best. The simple sliding window chunks leads to breaking of context - especially important for study notes.


# Day 3 Learnings

Today we implemented the search the functionality. I have a new-found respect for the search function that we use almost on very tool - the engineering marvel behind the scenes is just too good.

So 3 types of search methods were covered - essentially they are just 2 -> the third one is a combination of both.

1. Text Search
    - Simple to implement, fast, efficient and works well in most cases
    - Great to look up exact keyword matches, like when searching for a product by product ID
    - Fails for paraphrased queries
    - Does not consider the meaning or the intent of the query

2. Vector Search
    - This is something I have heard about but did not have any clue of it's working
    - The core idea of vector search is that the query is converted into a vector (aka embeddings) and matched with the content vectors - it finds semantically similar answers
    - For instance, if I search for canines - I'll get results of dogs, but with text search I wouldn't have any results returned unless the word 'canine' was part of the information.
    - However vector search fails where text search shines - exact match. Since vector search prioritizes summarsing the query, it does not perform well for exact searches.

The example below shows the strenghts and weaknesses of each method
| Query | Vector Search Result | Keyword Search Result |
| :--- | :--- | :--- |
| **"Acme Drill 500"** | Finds "Heavy-duty power tools" | Finds "Acme Drill 500" |
| **"Tool for making holes"** | Finds "Acme Drill 500" | Finds nothing (no match for "holes") |

3. Hybrid Search
Combining both approaches gives us the best of both worlds. This is known as "hybrid search".

For my personal project, where I'm building an AI agent on top of my data engineering / analytics engineering notes - both the text and vector search seem to perform decently. I'm curious how further down the course we would learn how to evaluate which search method works best for us.

# Day 4 Learnings
Today we actually built an AI agent - what's an agent?
An agent is a LLM that not only generates text but can also use tools - tools like searching the database for data, or running a Python script.
So LLM + Tool Access = Agent

Groq's documentation lists out the flow of how tools work with a LLMs

```
Your App → Makes request to Groq API with tool definitions   
   ↓ 
Groq API → Makes request to LLM model with user-provided tool definitions
         ← Model returns tool_calls (or, if no tool calls are needed, 
           returns final response)
   ↓
Your App → Parses tool call arguments
         → Executes function locally with provided arguments
         ← Function returns results
         → Makes request to Groq API with tool results 
   ↓
Groq API → Makes another request to LLM with tool results
         ← Model returns more tool_calls (returns to step 3), or 
           returns final response
   ↓
Your App
```

**Major components of tool use**

1. Tool Schema
    - You need to define what your tool does, give it a name, what parameters can it accept and so on
    - This is similar to the docstrings added to functions (Pydantic AI library actually uses those as the tool schema / definition)


2. System prompt
    - Contains the instructions for the LLM
    - You can explicilty state here to use tool XYZ
    - Therefore add clear instructions in your system prompts - what it needs to do, how it should do it, what to do if it fails etc

Finally I also learned about Pydantic AI library (ofc there's a python library to make your work easier). With the help of this library you do not need to explicitly handle the back and forth between LLM and tool. Pydantic provides a method called 'all_messages_json' - which basically returns the LLM's thinking mechanism. The output can show you where the tools were invoked, what were the parameters, how many times was it invoked and so on.

The part that was most fascinating to me was the multi-tool use from the LLM - it can not only invoke the tool once but multiple times (this depends on the system prompt) until it gets an answer or quits trying.


Groq documentation on tooling: https://console.groq.com/docs/tool-use/local-tool-calling#how-local-tool-calling-works


# Day 5 Learnings

Today I learnt how to evaluate the output of an AI agent. Essentially there are two methods, the first one is the manual check and the second one is a more comprehensive check wherein another LLM is used to evaulate the outcome and also used for generating test data.

## First Method of Evaluation - Logging + Manual Check

This is also called a "vibe check" - you simply ask the agent a few questions and evaluate the outcome manually. You might spot some edge cases that could be included in the system prompt or you might notice the agent hallucinates when XYZ is asked.

Manual evaluation will help you understand edge cases, learn what good responses look like and think of evaluation criteria for automated checks later.

So, in our case, we can have the following checks:
- Does the agent follow the instructions?
- Given the question, does the answer make sense?
- Does it include references?
- Did the agent use the available tools?


## Second Method of Evaluation - Use another LLM!

- LLMs can be used for judging the output for another LLM
- A key tip when using LLMs for judging -> make it give the justification before declaring the final results, this makes the LLM reason about the about before giving the final judgement.

So, in our case, we can have the following checks:
- Does the agent follow the instructions?
- Given the question, does the answer make sense?
- Does it include references?
- Did the agent use the available tools?

These questions can be converted into a checklist and the LLM can simply input 1/0.

This is helpful because then we can quantify "The agent followed the instructions 80% of the time."


Moreover, we also learnt today - how AI can be used for generating test scenarios

## Generating Test Data

We can use AI to generate questions by randomly referencing certain files and asking it to generate questions related to it. 

This approach provides us a ton of test data for evaluation but we also need to be careful since the AI might not consider how real users would ask questions

# Day 6 Learnings

For today lesson's the main focus was on deploying the AI agent - nobody wants to interact with it in a jupyter-notebook right?

So we built a modular python-streamlit based web app. Roughly it took me just 30 mins to get the app up and running. I remember when I first started out in data - without any AI tools - it used to take days to simple launch a streamlit app, but now I can do it with my phone.


