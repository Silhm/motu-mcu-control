

class Scribble:
    def __init__(self, screen_id=0):
        self.id = screen_id

    def full_text(self, text):
        print("Display {} on the full screen".format(text))

    def two_lines(self, l1, l2):
        print("first line   {}".format(l1))
        print("second line  {}".format(l2))

    def three_lines(self, header, l1, l2):
        print("Header line   {}".format(header))
        print("first  line   {}".format(l1))
        print("second line   {}".format(l2))


if __name__ == "__main__":
   print("scribble")
