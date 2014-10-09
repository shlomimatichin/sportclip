
_font = None

def _getFont():
    global _font
    if _font is None:
        _font = pygame.font.Font(None, 36)
    return _font


def blit(message
text = font.render(message, 1, (130, 130, 130))
            textpos = text.get_rect(centerx=self.background.get_width()/2)
            self.screen.blit(text, textpos)
#            self.graphSprite.draw(self.screen)
#            pos = audioPlayer.pos()
#            if pos is not None:
