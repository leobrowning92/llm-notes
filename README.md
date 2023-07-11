## TLDR


A set of tools with two guiding goals:
- perform bulk cleaning and modification of relational note data in my own personal notes in the zettelkasten style using, written in Obsidian Markdown.
- Use LLMs to perform those tasks, as a way to better understand these tools.

Note: although I will be using LLMs perhaps in situations where you dont strictly need to, I will be using them for a couple of tasks that would be difficult to do in another way on such a small corpus (1000s of small documents). E.g. adding tags to notes

## TODO

- [x] build code structures to load and parse the notes in a dumb manner, extracting document links, urls, tags, etc.
- [ ] construct and modify notes with frontmatter
- [ ] build a tagger to intelligently add tags to notes based of their semantic content, and the tags of other notes they link to. This could take the form of:
    - tag propogation using message passing ona graph, might satisfy #1, but not #2
    - zero shot classification using llms using the available tags to tag documents.
    - a little more of a complex workflow where llm embeddings are used to retrieve similar documents, and then assistant llms are used to consider if any of the tags on those documents are relevant to the current document
- [ ] build a filename shortener
    - [x] first with rules
    - [ ] then try constructing a prompt to get an llm to do it better, similar to variable names in code.
- [ ] build a url searcher and summarizer
    - [ ] code to fetch the url of a page. May need to consider common links like photos, twitter, podcasts, and blogs.
    - [ ] llm call to summarize the page, most likely from the raw html. (might want to consider chains for this?)




## Design

### Components

I think ill have a go at doing this manually and then with a langchain chain to see how it goes:
- consume text
- get adjacent notes
- determine if these notes are similar to the current note, and if so
- get similar text in vector store and consider the texts that are similar to the current text
- for both similar and linked notes, use the tags that are present in those notex, or the global set of tags as the space to tag from.
