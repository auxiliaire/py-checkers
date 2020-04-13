#-*-coding:utf-8;-*-
#qpy:2
#qpy:kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

from checkers.checkersengine import CheckersEngine

class CheckersTable(GridLayout):
    selected = ObjectProperty(None, allownone=True)
    
    def onReleaseHandler(self, cell):
        if self.selected == None:
            self.selectCell(cell)
        else:
            if CheckersEngine.isValidMove(self.ids, self.selected, cell):
                self.move(cell)
                self.selected = None
                CheckersEngine.checkGameOver(self.ids, self.onGameOver)
            else:
                self.cancelSelection()

    def selectCell(self, cell):
        if cell.text == CheckersEngine.O:
            self.selected = cell
            cell.text = CheckersEngine.X

    def move(self, cell):
        self.selected.text, CheckersEngine.getMiddleCell(self.ids, self.selected, cell).text, cell.text = CheckersEngine.MOVE

    def onGameOver(self, filled):
        checkersApp.resultScreen.stars.text = CheckersEngine.getStarsResult(filled)
        checkersApp.resultScreen.message.text = CheckersEngine.getMessage(filled)
        checkersApp.sm.transition.direction = 'left'
        checkersApp.sm.current = 'result'

    def cancelSelection(self):
        self.selected.text = CheckersEngine.O
        self.selected = None

class CheckersGame(BoxLayout):
    table = ObjectProperty(None)
    
    def reset(self):
        for cell in self.table.ids:
            self.table.ids[cell].text = CheckersEngine.O
        self.table.ids.cr3c3.text = ''
    
    def home(self):
        checkersApp.sm.transition.direction = 'right'
        checkersApp.sm.current = 'home'
    
    def info(self):
        checkersApp.sm.transition.direction = 'left'
        checkersApp.sm.current = 'help'

class HomeScreen(Screen):
    def leave(self):
        checkersApp.stop()

class GameScreen(Screen):
    game = ObjectProperty(None)
    
class ResultScreen(Screen):
    def leave(self):
        checkersApp.homeScreen.leave()
    
    def restart(self):
        checkersApp.gameScreen.game.reset()
        checkersApp.sm.transition.direction = 'right'
        checkersApp.sm.current = 'game'

class HelpScreen(Screen):
    def back(self):
        checkersApp.sm.transition.direction = 'right'
        checkersApp.sm.current = 'game'

class CheckersApp(App):
    sm = ObjectProperty(None)
    homeScreen = ObjectProperty(None)
    gameScreen = ObjectProperty(None)
    resultScreen = ObjectProperty(None)
    helpScreen = ObjectProperty(None)
    
    def build(self):
        self.sm = ScreenManager()
        self.homeScreen = HomeScreen(name='home')
        self.gameScreen = GameScreen(name='game')
        self.resultScreen = ResultScreen(name='result')
        self.helpScreen = HelpScreen(name='help')
        self.sm.add_widget(self.homeScreen)
        self.sm.add_widget(self.gameScreen)
        self.sm.add_widget(self.resultScreen)
        self.sm.add_widget(self.helpScreen)
        return self.sm
    
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
    
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            if self.sm.current == 'game':
                self.gameScreen.game.home()
                return True
            elif self.sm.current == 'result':
                self.resultScreen.restart()
                return True
            elif self.sm.current == 'help':
                self.helpScreen.back()
                return True
            else:
                self.stop()

class CIcon(Label):
    pass

class CButton(Button):
    pass
    
class UButton(Button):
    pass

if __name__ == '__main__':
    checkersApp = CheckersApp()
    checkersApp.run()
