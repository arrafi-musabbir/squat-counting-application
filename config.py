# minimum number of squats to get coins
squat_number = 10

dispenser = True

# minimum number ofccoins to  dispense at once
coins = 1

# timeout in seconds
timeout = 6

start_screen = "images/start screen.jpg"
prepare_screen = "images/prepare screen.jpg"
get_ready_screen = "images/get ready screen.jpg"
blank_screen = "images/blank screen.jpg"
finish_screen = "images/finish screen.jpg"

loading_gif = "images/loading.gif"

go_back = "images/back.png"


zero = "images/gugolas szamok-01.svg"
one = "images/gugolas szamok-02.svg"
two = "images/gugolas szamok-03.svg"
three = "images/gugolas szamok-04.svg"
four = "images/gugolas szamok-05.svg"
five = "images/gugolas szamok-06.svg"
six = "images/gugolas szamok-07.svg"
seven = "images/gugolas szamok-08.svg"
eight = "images/gugolas szamok-09.svg"
nine = "images/gugolas szamok-10.svg"


from num2words import num2words
def nwords(n):
    return globals()[num2words(n)]
