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

    def __str__(self):  # returns a str representation of length 2
        if type(self.value) == str:
            return self.value[0] + self.suit[0]
        return self.value[0] + self.suit[0]