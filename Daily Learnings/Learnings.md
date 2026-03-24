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
