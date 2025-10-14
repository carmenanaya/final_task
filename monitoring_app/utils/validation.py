def ask_alarm_level():
    try:
        level = int(input("Ställ in nivå för alarm mellan 1-100: "))
        if 1 <= level <= 100:
            return level
        else:
            print("Nivå måste vara mellan 1 och 100.")
            return None
    except ValueError:
        print("Ogiltig inmatning. Ange en siffra mellan 1 och 100.")
        return None

