from npl.vocabularise import Vocabularise


def main():
    
    with open( "assets/bookranger.txt", "r", encoding="utf-8" ) as file:
        booktext = file.read()
    
    corpus = [ booktext ]
    
    
    V = Vocabularise()
    
    regex = r'\d+\.\w+\.?\d*'
    

    vocab = V.vocabularise( corpus, tokeniser=V.PUNCTUATION_MID_WORD_ONLY, cleanup=regex )
    
    stemmedVocab, stemMap = V.stem( vocab )

    print( stemmedVocab )

    V.saveVocabulary( stemmedVocab )

if __name__ == '__main__': 
    main()