import argparse
import sys
import pygame
from pygame import locals
from moviepy import editor
import os
import interval

parser = argparse.ArgumentParser()
parser.add_argument("videoClip")
parser.add_argument("--jsonsDir", default="clips")
args = parser.parse_args()

if not os.path.isdir(args.jsonsDir):
    os.makedirs(args.jsonsDir)
clip = editor.VideoFileClip(args.videoClip)


class Main:
    _TEXT_COLOR = (130, 130, 130)
    _BACKGROUND_COLOR = (40, 40, 40)
    _PROGRESS_RECT = (10, 60, -20, 30)
    _PROGRESS_CENTER_Y = 75

    def __init__(self, width=1300, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.font = pygame.font.Font(None, 36)
        self.pos = 0
        self._intervals = {letter: interval.Interval(
            args.videoClip, args.jsonsDir, clip) for letter in (
                locals.K_a, locals.K_b, locals.K_c, locals.K_d, locals.K_e)}

    def _renderText(self, message, color):
        ANTI_ALIAS = 1
        return self.font.render(message, ANTI_ALIAS, color)

    def _processEvent(self, event):
        if event.type == pygame.QUIT:
            print "QUIT"
            sys.exit()
        elif event.type == locals.VIDEORESIZE:
            self._onResize(event.size)
            print "RESIZE", self.screen.get_size()
        elif event.type == locals.KEYDOWN:
            if event.key in [locals.K_RIGHT, locals.K_LEFT, locals.K_PAGEUP, locals.K_PAGEDOWN]:
                if event.key == locals.K_RIGHT:
                    self.pos += 1 / clip.fps
                elif event.key == locals.K_LEFT:
                    self.pos -= 1 / clip.fps
                elif event.key == locals.K_PAGEDOWN:
                    self.pos += 20 / clip.fps
                elif event.key == locals.K_PAGEUP:
                    self.pos -= 20 / clip.fps
                if self.pos > clip.duration:
                    self.pos = clip.duration
                if self.pos < 0:
                    self.pos = 0
                self._refreshVideoFrame()
            elif event.key == locals.K_q:
                print "Q - QUIT"
                sys.exit()
            elif event.key in self._intervals:
                self._intervals[event.key].setMarker(self.pos)

        elif event.type == locals.MOUSEBUTTONDOWN and event.button == 1:
            print "CLICK (%d, %d)" % event.pos
            if self._progressRect.collidepoint(event.pos):
                offset = event.pos[0] - self._progressRect[0]
                self.pos = clip.duration * offset / self._progressRect.width
                self._refreshVideoFrame()

    def _blitCentralizedMessageToScreen(self, message, yOffset):
        text = self._renderText(message, self._TEXT_COLOR)
        textpos = text.get_rect(centerx=self.background.get_width()/2)
        textpos[1] += yOffset
        self.screen.blit(text, textpos)

    def MainLoop(self):
        self._onResize(self.screen.get_size())
        self._refreshVideoFrame()

        while True:
            for event in pygame.event.get():
                self._processEvent(event)

            self.screen.blit(self.background, (0, 0))
            self._blitCentralizedMessageToScreen(args.videoClip, 0)
            message = "%dx%d %ffps %fs" % (
                clip.size[0], clip.size[1], clip.fps, clip.duration)
            self._blitCentralizedMessageToScreen(message, 30)
            self.screen.blit(self._videoFrame, (10, 90))
            self._drawPosLines()
            pygame.display.flip()

    def _drawPosLines(self):
        pygame.draw.line(
             self.screen, (10, 10, 10),
             self._progressRect.midleft, self._progressRect.midright, 1)
        x = self._progressRect.left + int(self.pos / clip.duration * self._progressRect.width)
        pygame.draw.line(
            self.screen, (200, 0, 0), (x, self._progressRect.top),
            (x, self._progressRect.bottom), 1)

    def _onResize(self, size):
        self.width, self.height = size
        self._progressRect = pygame.Rect(
            self._PROGRESS_RECT[0],
            self._PROGRESS_RECT[1],
            self._PROGRESS_RECT[2] + self.width,
            self._PROGRESS_RECT[3])
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.background = pygame.Surface(size)
        self.background = self.background.convert()
        self.background.fill(self._BACKGROUND_COLOR)
        clipSize = (1280, 640)
        self._resizedClip = clip.resize(clipSize)
        self._refreshVideoFrame()

    def _refreshVideoFrame(self):
        frame = self._resizedClip.get_frame(self.pos)
        self._videoFrame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
#        height = 90
#        width = self.screen.get_size()[0]
#        imageFile = tempfile.NamedTemporaryFile(suffix=".png")
#        wrapper.plot(args.soundtrackClip, width, height, imageFile.name)
#        image = pygame.image.load(imageFile.name).convert()
#        self.graph = pygame.sprite.Sprite()
#        self.graph.image = image
#        self.graph.rect = image.get_rect()
#        self.graph.rect.move_ip(0, 50);
#        self.graphSprite = pygame.sprite.RenderPlain(self.graph)


main = Main()
main.MainLoop()
