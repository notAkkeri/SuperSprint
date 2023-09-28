import sys
import pygame
from pygame.locals import *
from button import Button
from misc import get_font, click_sound, drawOver, drawScore2, drawHighscoreText, drawNewHS, endBG, gameOverTheme

pygame.init()
pygame.mixer.init()

class EndScreen:
    def __init__(self, SCREEN, game_state_manager):
        self.SCREEN = SCREEN
        self.game_state_manager = game_state_manager
        self.endScreen = True
        self.current_score = 0
        self.high_score = 0
        self.new_high_score = False
        self.game_over_theme_playing = False  
        self.game_over_theme = None
 

    def load_scores(self):
        try:
            with open("Scores/currentScore.txt", "r") as file:
                self.current_score = int(file.readline())
        except FileNotFoundError:
            self.current_score = 0

        try:
            with open("Scores/scores.txt", "r") as file:
                self.high_score = int(file.readline())
        except FileNotFoundError:
            self.high_score = 0

    def update_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            with open("Scores/scores.txt", "w") as file:
                file.write(str(self.high_score))
            self.new_high_score = True

    def drawNewHS(self):
        new_high_score_text = get_font(35).render("New High Score!", True, (255, 0, 0))
        new_high_score_rect = new_high_score_text.get_rect(center=(self.SCREEN.get_width() // 2, 450))
        self.SCREEN.blit(new_high_score_text, new_high_score_rect)

    def play_game_over_theme(self):
        if not self.game_over_theme_playing:
            self.game_over_theme = gameOverTheme()  
            self.game_over_theme.play()
            self.game_over_theme_playing = True

    def stop_game_over_theme(self):
        if self.game_over_theme_playing and self.game_over_theme:
            self.game_over_theme.stop()
            self.game_over_theme_playing = False

    def run(self):
        # load score txt files
        self.load_scores()
        self.new_high_score = False
        self.update_high_score()  # check if a new high score
        self.play_game_over_theme() # plays theme 
        while self.endScreen:
            self.SCREEN.fill((0, 0, 0))
            # Background
            self.SCREEN.blit(endBG, (0, 0))
            pygame.display.set_caption("Game Over")
            endMouse = pygame.mouse.get_pos()

            # TEXT
            drawOver(self.SCREEN, 400, 0)

            # HS check 
            if self.new_high_score:
                drawNewHS(self.SCREEN, f"New High Score: {self.high_score}", 680, 240)
            else:
                drawHighscoreText(self.SCREEN, f"High Score: {self.high_score}", 660, 200)
                drawScore2(self.SCREEN, self.current_score, 420, 300)
            
            # Buttons
            exitButton = Button(image=pygame.image.load("assets/rect3.png"), pos=(750, 600),
                                text_input="Exit", font=get_font(25), base_color="#f1e8ef", hovering_color="#1b1018",
                                click_sound=click_sound)
            
            againButton = Button(image=pygame.image.load("assets/rect3.png"), pos=(550, 600),
                                text_input="Play Again", font=get_font(25), base_color="#f1e8ef", hovering_color="#1b1018",
                                click_sound=click_sound)

            for button in [againButton, exitButton]:
                button.changeColor(endMouse)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if againButton.checkForInput(endMouse):
                        click_sound.play()
                        self.endScreen = False
                        self.stop_game_over_theme()  # Stop the game over theme
                        self.game_state_manager.set_state("game", self.SCREEN, self.game_state_manager)
                        return
                    if exitButton.checkForInput(endMouse):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    end_screen = EndScreen(SCREEN, None)

    while True:
        end_screen.run()
