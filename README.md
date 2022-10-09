# nlputils
Utilites for processing various types of data for machine learning models


## Functionality

### Vocabularise

It helps build and manager vocabularies from corpi. It includes the following functionality:

1. tokenise (Useful regex: r"([\w]+(?:(?!\s)\W?[\w]+)*)" )
2. stem or unstem
3. filters: ability to define filters that will accept or reject vocabulary entries (e.g. stopwords)	
4. token-level cleanups
5. merging of multiple vocabularies
6. Replace character(s) in all token
7. Save vocabulary
8. Load vocabulary

### Frequentise

Utility to build and manage frequency matrices from corpi with the following functionality:

1. turn corpus into frequncy matrix ( corpus, vocab )
2. merge multiple vocabs and freq matrices together


