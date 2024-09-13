from itertools import islice
from pathlib import Path
import os


FONT = {
    "a": "A40408 080CAC ECE8E4",
    "b": "04E4E8 E8EC0C 04040F",
    "c": "E40408 080CEC 080CAC",  # TODO: make more round ?
    "d": "E40408 080CEC E4E4EF",
    "e": "E40408 081DEA EAE748",
    "f": "787FEF 787000 0B0BEB",
    "g": "840408 083DEA E8E070",
    "h": "E4E4E8 E8EC0C 04040F",
    "i": "8E8E8E 8E8E8E 6B14C4",
    "j": "8E8E8E 5BACA9 A9A000",
    "k": "04040F 082BEC 0749E4",
    "l": "4833A4 484F8F 9FFC06",
    # "m": "043F6A 6A708A 8ABFE4",
    "m": "040409 0C7C74 8CEDE4",
    "n": "040404 04040C 3BFEE4",
    # "o1": "E8DD2B 0B0535 35C3E8",
    "o": "E8DD2B 080635 35C3E8",
    # "o3": "E8AF19 080635 35C3E8",
    "p": "04E4E8 E8EC0C 00040C",
    "q": "E40408 080CEC E0E4EC",
    "r": "040404 04040C 4AFEEA",
    "s": "0573E5 E50B0B 0B7EEB",
    "t": "68688E 6864C4 0B0BEB",
    "u": "0C0C0C 0C0474 74E4EC",
    "v": "0C0C0C 0C5474 7494EC",
    "w": "0C2056 96C0EC 567996",
    "x": "040404 04A80C E458EC",
    "y": "0C0284 ECE4E4 E4E020",
    "z": "0CECEB 0677EA 0504E4",
    "?": "646464 67E8E9 5EFEEA",
    "H": "04040F 0B8AEB E4E4EF",
    "I": "3434B4 74747F 3F3FBF",
    "!": "646464 673F6F 67AF6F",
    ".": "545454",
    ",": "446452",
    "P": "04040F 0FEFEC ECE909",
    "'": "4C6C5A",
    # "aa": "A40408 080CAC ECE8E4" ,
}


def chunked(iterable, n: int):
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


for character in [list(FONT.values())[-1]]:
    points = []
    for bezier in character.split():
        x0, y0, x1, y1, x2, y2 = [int(x, 16) / 15 for x in (bezier * 3)[:6]]
        x0, x1, x2 = [0.1 + 0.8 * 16 / 15 * x for x in [x0, x1, x2]]
        y0, y1, y2 = [0.1 + 1.8 * y for y in [y0, y1, y2]]
        for alpha in range(100):
            t = alpha / 99
            points.append(
                (
                    (1 - t) * ((1 - t) * x0 + t * x1) + t * ((1 - t) * x1 + t * x2),
                    (1 - t) * ((1 - t) * y0 + t * y1) + t * ((1 - t) * y1 + t * y2),
                )
            )
    try:
        h = os.get_terminal_size().lines - 1
    except OSError:
        h = 155 - 1
    w = (h + 1) // 2
    image = []
    for y in reversed(range(h)):
        image_row = "·"
        cell = "··" if y in (0, h - 1, round(h / 20), round(0.29 * h), round(0.7563 * h), round(0.95 * h)) else "  "
        for x in range(w):
            distance = min(((px - x / (w - 1)) ** 2 + (py - y / (w - 1)) ** 2) ** 0.5 for px, py in points)
            image_row += "██" if distance < 0.1 else cell
        image_row += "·"
        image.append(image_row)
    print("\n".join(image))


binary = bytearray()
letters = "abcdefghijklmnopqrstuvwxyz.!HI,P'"
for char in letters + "?" * (64 - len(letters)):
    beziers = FONT.get(char, FONT["?"]).split()
    while len(beziers) < 3:
        beziers = [beziers[0][0:2] * 3] + beziers
    binary.extend(b"".join(bytes(int("".join(byte), 16) for byte in chunked(bezier, 2)) for bezier in beziers))

Path(Path(__file__).resolve().parent.parent, "static/font.bin").write_bytes(binary)
