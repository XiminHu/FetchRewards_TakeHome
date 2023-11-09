Writeup for the take-home

Primary goal: design a search tool to retrieve offers

Input: Query text
Output: Offers and similarity scores

Due to the small size of the given datasets, it is proper and reasonable to deploy smaller scale methods rather than large NLP models (e.g., word2Vec). Therefore, I chose fuzzy for the search and similarity score calculation. The assumption is that users will have an clear idea of their searching (i.e., the range of query text is bounded) target instead of 'browsing' type of searching (i.e., the query text will be unbounded).

If larger dataset is offered, a few other methods would be benificial, including TF-IDF, word2Vec to increase the matching accuracy and facilitate fuzzy search. It would also improve the similarity score calculation process.

For deploying the tool, I was focusing on the backend, and to minimize the cost of development and debugging, I decided to have a CLI tool. For future development, if time is permitted, further front-end works would be benificial (e.g., hosting a website).


