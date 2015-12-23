import math

class id_handler:
    """
    Class for encoding and decoding ID's for pictures.
    From: http://kvz.io/blog/2009/06/10/create-short-ids-with-php-like-youtube-or-tinyurl/
    """

    def __init__(self, max_len):
        self.ALPHABET = "bcdfghjklmnpqrstvwxyz0123456789BCDFGHJKLMNPQRSTVWXYZ"
        self.BASE = len(self.ALPHABET)
        self.MAXLEN = max_len

    def encode_id(self, n):

        pad = self.MAXLEN - 1
        n = int(n + pow(self.BASE, pad))

        s = []
        t = int(math.log(n, self.BASE))
        while True:
            bcp = int(pow(self.BASE, t))
            a = int(n / bcp) % self.BASE
            s.append(self.ALPHABET[a:a+1])
            n = n - (a * bcp)
            t -= 1
            if t < 0: break

        return "".join(reversed(s))

    def decode_id(self, n):
            
        n = "".join(reversed(n))
        s = 0
        l = len(n) - 1
        t = 0
        while True:
            bcpow = int(pow(self.BASE, l - t))
            s = s + self.ALPHABET.index(n[t:t+1]) * bcpow
            t += 1
            if t > l: break

            pad = self.MAXLEN - 1
            s = int(s - pow(self.BASE, pad))

        return int(s)
