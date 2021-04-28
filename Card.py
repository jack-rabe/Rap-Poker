import pygame
import io


class Card:
    def __init__(self, image, value, suit, session):
        self.value = value
        self.suit = suit

        # convert the image to a file-like object and load it using pygame
        image_url = session.get(image)
        img = io.BytesIO(image_url.content)
        temp_image = pygame.image.load(img)
        self.image = pygame.transform.rotozoom(temp_image, 0, 0.4)

    def __str__(self):  # returns a str representation of length 2 (0? for a 10)
        value = self.value[0] if self.value != "10" else "0"
        return value + self.suit[0]

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        royalty = "JQKA"
        val = self.value[0] if self.value.isalpha() else self.value
        other_val = other.value[0] if other.value.isalpha() else other.value
        if val in royalty:
            val = 11 + royalty.index(val)
        if other_val in royalty:
            other_val = 11 + royalty.index(other_val)

        if int(val) - int(other_val) >= 0:
            return False
        else:
            return True