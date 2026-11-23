#!/usr/bin/env python3
"""Render the 22 November 2026 front page as a 1024x1024 PNG.

Build-time only: Pillow plus the standard library. The shipped program
(main.py) is stdlib-only; this file is only used to produce entry.png.

Every picture element is drawn with Pillow shapes and text -- there are no
photographs and no borrowed artwork. The news items below were checked
against live sources on 2026-11-22 around 14:10 UTC:

  * COP31 in Antalya ended without a fossil-fuel deal after the EU
    objected to a final draft that never mentions fossil fuels.
  * Iran struck a civilian site in Bahrain and US bases, and said it
    destroyed two US Patriot radars; two tankers were hit near Hormuz.
  * Mexican special forces captured Fausto Isidro Meza Flores
    ("El Chapo Isidro") in Sinaloa; 11 people were killed.
  * A Russian missile hit Kryvyi Rih, killing 2 and wounding 60, and a
    Russian cargo ship caught fire after a drone strike.
  * US stocks fell into correction: S&P 500 -3.7%, Nasdaq -5.3%.
  * The EU and Indonesia signed a trade deal after almost ten years of
    talks, scrapping tariffs on up to 98.5% of goods.
  * Briefs: GTA VI set a $3.79bn launch-day record; a candy factory
    fire in Cikande, Indonesia killed 3 and left 36 missing.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Palette, kept as a small dictionary so the whole page shares one scheme.
PALETTE = {
    "paper": (250, 248, 242),
    "navy": (11, 31, 58),
    "crimson": (178, 34, 34),
    "gold": (201, 162, 39),
    "ink": (20, 20, 20),
    "grey": (70, 70, 70),
    "panel": (232, 236, 242),
    "rule": (180, 180, 180),
    "teal": (0, 110, 60),
    "plum": (120, 40, 140),
    "white": (255, 255, 255),
}


def load_font(path, size):
    """Load a DejaVu font at the requested point size."""
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, width):
    """Split text into lines that fit inside width pixels.

    A single word wider than the column is split character by character
    instead of overflowing the card.
    """
    lines = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
            while draw.textlength(current, font=font) > width and len(current) > 1:
                cut = 1
                while (cut < len(current)
                       and draw.textlength(current[:cut], font=font) <= width):
                    cut += 1
                lines.append(current[:cut - 1])
                current = current[cut - 1:]
    if current:
        lines.append(current)
    return lines


class FrontPage:
    """A drawable front page with a masthead, story cards and briefs."""

    def __init__(self):
        self.image = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
        self.draw = ImageDraw.Draw(self.image)

    def paragraph(self, x, y, text, font, colour, width, leading=None):
        """Draw wrapped text and return the y coordinate below it."""
        step = leading if leading is not None else int(font.size * 1.22)
        for line in wrap_text(self.draw, text, font, width):
            self.draw.text((x, y), line, font=font, fill=colour)
            y += step
        return y

    def banner(self, x, y, w, label, fill):
        """Draw a coloured label strip at the top of a story card."""
        self.draw.rectangle([x, y, x + w, y + 32], fill=fill)
        self.draw.text((x + 12, y + 6), label, font=load_font(BOLD_PATH, 20),
                       fill=PALETTE["white"])

    def card(self, x, y, w, h, tag, fill, headline, body,
             head_size=25, body_size=19):
        """Draw one bordered story card with a label, headline and body."""
        self.draw.rectangle([x, y, x + w, y + h], outline=PALETTE["rule"], width=2)
        self.banner(x, y, w, tag, fill)
        bottom = self.paragraph(x + 14, y + 42, headline,
                                load_font(BOLD_PATH, head_size),
                                PALETTE["ink"], w - 28)
        self.paragraph(x + 14, bottom + 6, body,
                       load_font(PLAIN_PATH, body_size),
                       PALETTE["grey"], w - 28)

    def masthead(self):
        """Draw the navy masthead bar with the paper name and date."""
        self.draw.rectangle([0, 0, PAGE_W, 128], fill=PALETTE["navy"])
        self.draw.rectangle([0, 128, PAGE_W, 134], fill=PALETTE["gold"])
        self.draw.text((32, 18), "THE WORLD IN ONE PAGE",
                       font=load_font(BOLD_PATH, 52), fill=PALETTE["white"])
        self.draw.text((32, 82), "Sunday 22 November 2026",
                       font=load_font(BOLD_PATH, 30), fill=PALETTE["gold"])
        self.draw.text((700, 84), "WORLD NEWS",
                       font=load_font(BOLD_PATH, 28), fill=PALETTE["white"])

    def lead(self):
        """Draw the lead story box under the masthead."""
        self.draw.rectangle([24, 152, 1000, 400], outline=PALETTE["rule"], width=2)
        self.draw.rectangle([24, 152, 150, 186], fill=PALETTE["crimson"])
        self.draw.text((36, 158), "LEAD", font=load_font(BOLD_PATH, 22),
                       fill=PALETTE["white"])
        end = self.paragraph(40, 194, "COP31 talks end with no fossil-fuel deal",
                             load_font(BOLD_PATH, 44), PALETTE["ink"], 940)
        self.paragraph(40, end + 8,
                       "Climate talks in Antalya close with no agreement after "
                       "the EU objected to a final draft that never mentions "
                       "fossil fuels.",
                       load_font(PLAIN_PATH, 23), PALETTE["grey"], 940)

    def build(self):
        """Lay out every section and return the finished image."""
        self.masthead()
        self.lead()

        middle = [
            ("GULF", PALETTE["crimson"], "Iran strikes Bahrain and US bases",
             "Iran hit a civilian site in Bahrain and says it destroyed two "
             "US Patriot radars. Two tankers were hit near Hormuz."),
            ("MEXICO", PALETTE["navy"], "Cartel boss 'El Chapo Isidro' captured",
             "Mexican special forces seized Fausto Isidro Meza Flores in "
             "Sinaloa. Eleven people were killed, four of them soldiers."),
            ("MARKETS", PALETTE["teal"], "US stocks fall into correction",
             "The S&P 500 fell 3.7% on Friday and the Nasdaq 5.3% as the AI "
             "sell-off spread to Japan and Korea."),
        ]
        for index, (tag, colour, headline, body) in enumerate(middle):
            self.card(24 + index * 326, 416, 302, 262, tag, colour,
                      headline, body)

        lower = [
            ("UKRAINE", PALETTE["navy"], "Russian missile hits Zelenskyy's hometown",
             "A strike on Kryvyi Rih killed two and wounded 60; a Russian "
             "cargo ship burns.", 29, 20),
            ("TRADE", PALETTE["plum"], "EU and Indonesia sign landmark trade deal",
             "After almost ten years of talks, the deal scraps tariffs on up "
             "to 98.5% of goods.", 29, 20),
        ]
        for index, (tag, colour, headline, body, hs, bs) in enumerate(lower):
            self.card(24 + index * 490, 694, 466, 184, tag, colour,
                      headline, body, head_size=hs, body_size=bs)

        self.draw.rectangle([24, 894, 1000, 978], fill=PALETTE["panel"])
        self.draw.text((40, 904), "IN BRIEF", font=load_font(BOLD_PATH, 22),
                       fill=PALETTE["crimson"])
        self.draw.text((40, 930), "GTA VI sets a $3.79bn launch-day record.",
                       font=load_font(PLAIN_PATH, 20), fill=PALETTE["ink"])
        self.draw.text((40, 954),
                       "Candy factory fire in Indonesia kills 3; 36 still missing.",
                       font=load_font(PLAIN_PATH, 20), fill=PALETTE["ink"])
        # Thin gold rule separating the briefs panel from the footer line.
        self.draw.rectangle([32, 986, 992, 988], fill=PALETTE["gold"])
        self.draw.text((32, 992), "22 November 2026  •  The world in one page",
                       font=load_font(PLAIN_PATH, 20), fill=PALETTE["grey"])
        return self.image


def main():
    page = FrontPage()
    picture = page.build()
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    picture.save(target, optimize=True)
    print(target, picture.size, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
