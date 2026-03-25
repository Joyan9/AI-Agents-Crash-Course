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

So  types of search methods were covered, essentially they are just 2 - the third one is a combination of both.

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
Combining both approaches gives us the best of both worlds. This is known as "hybrid search."

