import paralleldots

paralleldots.set_api_key('5IAudGuShdT5PDelXQ9MVwurzPg1f5gsYBl5bLzULTE')
paralleldots.get_api_key()

text1  = "Chipotle in the north of Chicago is a nice outlet. I went to this place for their famous burritos but fell in love with their healthy avocado salads. Our server Jessica was very helpful. Will pop in again soon!"
text2 = "its a nice day"
text3 = "fuck"
text4 = "you are so good"
text5 = "mother fuck"
text6 = "you are so fucking great"
result  = paralleldots.abuse(text6)
if (result['abusive'] > 0.9 or result['hate_speech'] >0.9):
    print("sad")
else:
    print("happy")