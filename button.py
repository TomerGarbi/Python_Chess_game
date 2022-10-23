import pygame


class Button:
    def __init__(self, height, width, color, position, text, return_value):
        self.height = height
        self.width = width
        self.color = color
        self.position = position
        self.text = text
        self.return_value = return_value

    def set_color(self, new_color):
        self.color = new_color

    def hover_button(self, mouse):
        if self.position[0] <= mouse[0] <= self.position[0] + self.height:
            if self.position[1] <= mouse[1] <= self.position[1] + self.width:
                return True
        return False
