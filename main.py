#-*-coding:utf8;-*-
#qpy:2
#qpy:kivy

from kivy.app import App
from kivy.uix.label import Label
#from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

class CIcon(Label):
    pass

class CButton(Button):
    pass
    
class UButton(Button):
    pass

class CheckersTable(GridLayout):
    O = chr(0xf111)
    X = chr(0xf1db)
    STAR = chr(0xf005)
    HOLE = chr(0xf006)
    MSG = '{filled} button{pm} remained.'
    GOAL = '\n[b]Try to achieve three or less to earn stars![/b]'
    COMMENTS = {
    	    3: '\n[b]Not bad![/b]',
    	    2: '\n[b]Well done![/b]',
    	    1: '\n[b]Perfect![/b]'
    	}
    
    selected = ObjectProperty(None, allownone=True)
    betweener = ObjectProperty(None, allownone=True)
    
    def isValidMove(self, obj):
        valid = False
        self.betweener = None
        if self.selected != None:
            sourceRow = self.selected.row
            sourceCol = self.selected.col
            targetRow = obj.row
            targetCol = obj.col
            valid = ((sourceRow == targetRow
            	    and abs(sourceCol - targetCol) == 2)
            	  or (sourceCol == targetCol
            	    and abs(sourceRow - targetRow) == 2)
            	)
            if valid:
            	    betweener = self.ids["cr{0}c{1}".format(int((sourceRow + targetRow) / 2), int((sourceCol + targetCol) / 2))]
            	    valid = valid and betweener.text == self.O
            	    if valid: self.betweener = betweener
        return valid
    
    def isOver(self):
        temp = self.selected
        for source in self.ids:
            if self.ids[source].text == self.O:
                self.selected = self.ids[source]
            for dest in self.ids:
                if self.ids[dest].text == '':
                    if self.isValidMove(self.ids[dest]):
                        self.selected = temp
                        return False
        self.selected = temp
        return True
    
    def getCountFilled(self):
        cnt = 0
        for cell in self.ids:
            if self.ids[cell].text == self.O:
                cnt = cnt + 1
        return cnt
    
    def getMessage(self, filled):
        pm = ''
        if filled > 1:
            pm = 's'
        return self.MSG.format(filled = filled, pm = pm)
    
    def onReleaseHandler(self, obj):
        if self.selected == None:
            if obj.text == self.O:
                self.selected = obj
                obj.text = self.X
        else:
            if obj.text == '' and self.isValidMove(obj):
                self.selected.text = ''
                self.selected = None
                self.betweener.text = ''
                self.betweener = None
                obj.text = self.O
                if self.isOver():
                    filled = self.getCountFilled()
                    msg = self.getMessage(filled)
                    if filled < 4:
                        checkersApp.resultScreen.stars.text = (self.STAR * ((4 - filled) % 4)).ljust(3, self.HOLE)
                    else:
                        checkersApp.resultScreen.stars.text = self.HOLE * 3
                    msg += self.COMMENTS.get(filled, self.GOAL)
                    checkersApp.resultScreen.message.text = msg
                    checkersApp.sm.transition.direction = 'left'
                    checkersApp.sm.current = 'result'
            else:
                self.selected.text = self.O
                self.selected = None

class CheckersGame(BoxLayout):
    table = ObjectProperty(None)
    
    def reset(self):
        for cell in self.table.ids:
            self.table.ids[cell].text = self.table.O
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

if __name__ == '__main__':
    checkersApp = CheckersApp()
    checkersApp.run()
