from misc import *

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, click_sound):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.click_sound = click_sound

	# Updates button & bltiz the button onto screen
	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)
	# Searches for (X,Y) within the button bounds & returns true if (X,Y) is within, else false
	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
	# Changes color of the button depending on mouse hover & locates current mouse positon (x,y)
	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			# if mouse is hovering over the buttons 
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			# if mouse not hovering over the button
			self.text = self.font.render(self.text_input, True, self.base_color)

	def handle_click(self):
		click_sound.play()

