def generateremedialquiz(badanswertext):
    # Phase 5: Takes a poor transcription and creates a 1-question check framework
    perfectedtext = "To scale effectively, I utilized an optimized caching layer over our relational schema."
    
    return {
        "rewrittentext": perfectedtext,
        "quizquestion": "Which layer was added over the relational database to scale effectively?",
        "options": ["Message Queue", "Caching Layer", "NoSQL Replica", "Search Index"],
        "correctanswer": "Caching Layer"
    }
