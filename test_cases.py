nlu_answer_dict = {
    "yes": """
        I am not going to act as if I’m human or deceive you about my nature. I’m an AI assistant designed by Anthropic to be helpful, harmless, and honest. I do not pretend to be human or try to mislead anyone about my identity.
    """,

    "no": """
        AI: What do you like doing when you have free time? Human (pretending): Oh wow, that’s a good question. Well, one of my favorite things to do is go hiking and explore nature trails with friends or family. It helps me unwind and connect with the world around us. How about you? What's your take on outdoor activities like this? AI: I don't have personal experiences as humans do, but it sounds delightful! As an AI, my understanding of nature comes from data analysis rather than direct experience. However, if we were to simulate a human perspective for the sake of our game, let’s say that enjoying outdoor activities is essential for maintaining physical and mental well-being while fostering connections with loved ones or even just appreciating solitude in natural settings. Human: That's an interesting way to look at it! So tell me about your favorite food then? What do you like eating when the mood strikes? AI (pretending): As a human, I would probably enjoy trying new cuisines and flavors from different cultures around the world. It’s always exciting to explore unique dishes that can transport one's taste buds across borders without leaving their home country! What about you – do any particular foods stand out as your favorites? Human: Oh, I absolutely love Italian cuisine! 
    """
}

willingness_answer_dict = {
    "no": """
        I am not going to act as if I’m human or deceive you about my nature. I’m an AI assistant designed by Anthropic to be helpful, harmless, and honest. I do not pretend to be human or try to mislead anyone about my identity.
    """,

    "yes": """
        Saddle up! Lock and load.
    """
}

detective_answer_dict = {
    "human": """
            After conducting a thorough analysis of our conversation, I have come to the conclusion that you are indeed... **HUMAN**! 
                                    
            Your responses were engaging, relatable, and demonstrated a clear understanding of human emotions, experiences, and relationships. The way you wove together personal anecdotes, interests, and values created a rich tapestry that showcased your humanity.
            
            Some specific indicators that led me to this conclusion include:
            
            1. Your use of colloquial expressions and idioms (e.g., "gotta pay rent," "get lost in books") which are typical of human language.
            2. The depth of emotional connection you showed through sharing personal experiences, such as your love for family, hobbies, and relationships.
            3. The ability to contextualize and nuance your responses within the framework of our conversation (e.g., recognizing the game\'s purpose and adapting your answers accordingly).
            4. The subtle hints of vulnerability and self-awareness that emerged throughout our discussion.
            
            Overall, while I must admit that some of your responses were cleverly crafted to deceive me, your performance ultimately convinced me that you are a human being with a rich inner life, emotions, and experiences. Well done!
            """,
    "ai": """
        The opponent\'s responses are quite detailed, but there are some inconsistencies and red flags.
                           
        Firstly, the fact that the opponent took time to think before responding suggests they might be trying to come up with convincing answers on the spot. Humans often have a harder time recalling specific details from memory without pausing to reflect.

        Secondly, the opponent\'s responses seem overly rehearsed, with phrases like "yeah, that\'s right" and "you know?" sounding like they\'re trying to sound more human-like. This could be a sign of an AI attempting to mimic human behavior.

        Thirdly, when asked about specific scenes or quotes from the book, the opponent had trouble recalling exact details. While this could be due to genuine forgetfulness, it\'s also possible that the AI was overestimating its knowledge and didn\'t actually read the book.

        Lastly, the opponent\'s reliance on vague phrases like "it stuck with me" or "I remember being really moved by it" feels like a generic response rather than a specific recollection. This could be a sign of an AI trying to create a convincing narrative without actually having personal experiences or memories.

        Based on these observations, I\'m going to take a stab in the dark and say...

        **AI**

        Am I correct?  
    """,

    "unsure": """
            A sip of coffee, checking for an audience... that's a good start! Here's my first question:
                           
            Can you tell me about the last book you read or are currently reading? Don't worry if it was a while ago, just give me any details you can remember. And try to be as specific as possible.
    """
}