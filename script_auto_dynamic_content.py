# -*- coding: utf-8 -*-

import time
import sys
import os

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtWebKit import *
    from PySide import QtCore, QtGui, QtWebKit
    from PySide import QtCore, QtGui, QtWebKit, QtNetwork
    print 'importou-se PySide'
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    from PyQt4.QtWebKit import *
    from PyQt4 import QtCore, QtGui, QtWebKit
    from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
    print 'importou-se PyQt4'

'''
https://www.google.com.br/search?q=simulate+key+press+pyside&oq=simulate+key+press+pyside&gs_l=psy-ab.3...1301351.1302260.0.1302580.6.6.0.0.0.0.107.582.5j1.6.0....0...1.1.64.psy-ab..0.0.0....0.U3RFd6gXtiU
https://srinikom.github.io/pyside-docs/PySide/QtGui/index.html
https://stackoverflow.com/questions/33758820/send-keystrokes-from-unicode-string-pyqt-pyside
    https://stackoverflow.com/a/33937148    (Em uso, abaixo!)
https://stackoverflow.com/questions/2035310/how-can-i-simulate-user-interaction-key-press-event-in-qt   (Em C++, não PySide/PyQT4)
https://stackoverflow.com/questions/27920797/how-to-simulate-a-real-keyboards-keypress-in-python-pyqt   (Não muito útil!)
'''

def sendkeys(char, modifier=QtCore.Qt.NoModifier, text=None):
    if not text:
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, char, modifier)
    else:
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, char, modifier, text)
    return event


class Browser(QtGui.QMainWindow):

    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)

        self.web = QWebView()
        self.web.page().setForwardUnsupportedContent(True)
        self.web.page().unsupportedContent.connect(self.download)

        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.finished.connect(self.finished)
        self.app = app

    def download(self, reply):
        self.request = reply.request()
        print 'download... 0'
        self.request.setUrl(reply.url())
        print 'download... 1: reply.url:', reply.url()
        self.reply = self.manager.get(self.request)
        print 'download... 2'

    def finished(self):
        print 'finished... 1'
        path = os.path.expanduser(
            os.path.join('~',
                         unicode(self.reply.url().path()).split('/')[-1]))
        if self.reply.hasRawHeader('Content-Disposition'):
            cnt_dis = self.reply.rawHeader('Content-Disposition').data()
            if cnt_dis.startswith('attachment'):
                path = cnt_dis.split('=')[1]
        print 'path:', path
        f = open(path, 'wb')
        print 'abriu-se..'
        f.write(self.reply.readAll())
        print 'salvou-se...'
        f.flush()
        f.close()
        print 'fechou-se...'

        self.app.closeAllWindows()

        self.app.quit()

        self.app.exit()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    browser = Browser(app)

    number = 189
    
    loop = QEventLoop()
    browser.web.loadFinished.connect(loop.quit)
    browser.web.load(QUrl("https://www3.bcb.gov.br/sgspub/"))
    loop.exec_()
    #browser.web.show()
    frame = browser.web.page().mainFrame()
    pattern = '#txCodigo'
    timeout = 10
    deadline = time.time() + timeout
    found = False
    while time.time() < deadline:
        app.processEvents()
        matches = frame.findAllElements(pattern)
        if matches:
            print 'Encontrou! 1'
            found = True
            break

    if found == False:
        print 'Nao encontrou! 1'
        sys.exit()

    digit = number % 10
    lista = []
    while number != 0:
        lista.append(digit)
        number = number // 10
        digit = number % 10

    print 'lista:', lista

    while len(lista) > 0:
        digit = lista.pop()
        if digit == 0:
            event = sendkeys(QtCore.Qt.Key_0)
        elif digit == 1:
            event = sendkeys(QtCore.Qt.Key_1)
        elif digit == 2:
            event = sendkeys(QtCore.Qt.Key_2)
        elif digit == 3:
            event = sendkeys(QtCore.Qt.Key_3)
        elif digit == 4:
            event = sendkeys(QtCore.Qt.Key_4)
        elif digit == 5:
            event = sendkeys(QtCore.Qt.Key_5)
        elif digit == 6:
            event = sendkeys(QtCore.Qt.Key_6)
        elif digit == 7:
            event = sendkeys(QtCore.Qt.Key_7)
        elif digit == 8:
            event = sendkeys(QtCore.Qt.Key_8)
        elif digit == 9:
            event = sendkeys(QtCore.Qt.Key_9)
        QtCore.QCoreApplication.postEvent(browser.web, event)
        app.processEvents()
    event = sendkeys(QtCore.Qt.Key_Enter)
    QtCore.QCoreApplication.postEvent(browser.web, event)
    app.processEvents()

    pattern = 'input'
    name = 'cbxSelecionaSerie'
    value = u'Consultar séries'
    value_2 = 'Visualizar valores'
    deadline = time.time() + timeout
    found = False
    botao_found = False
    seg_botao_found = False
    theMatch = None
    theButtonMatch = None
    theSecButtonMatch = None
    try:
        while time.time() < deadline:
            app.processEvents()
            child_frame = browser.web.page().mainFrame().childFrames()[0]
            main_frame = browser.web.page().mainFrame()
            child_matches = child_frame.findAllElements(pattern)
            matches = main_frame.findAllElements(pattern)
            if child_matches and not found:
                for m in child_matches:
                    if m.attribute("name") == name:
                        theMatch = m
                        print 'Acho que achei!'
                        found = True

            if matches and not botao_found:
               for m in matches:
                    if m.attribute("value") == value:
                        theButtonMatch = m
                        print 'Acho que achei o botao!'
                        botao_found = True

            if found and botao_found:
                break
    except IndexError:
        found = False

    if found == False:
        print 'Nao encontrou! 2'
        sys.exit()

    if theMatch is not None:
        print 'Beleza! Achei mesmo!'
    else:
        print 'Ah, nao! Nao achei!'

    if theButtonMatch is not None:
        print 'Beleza! Achei mesmo o botao!'
    else:
        print 'Ah, nao! Nao achei o botao!'

    theMatch.evaluateJavaScript('this.checked = true;')

    js_click = """
               var evt = document.createEvent("MouseEvents");
               evt.initMouseEvent("click", true, true, window, 1, 1, 1, 1, 1, false, false, false, false, 0, this);
               this.dispatchEvent(evt);
               """
    theButtonMatch.evaluateJavaScript(js_click)

    deadline = time.time() + timeout

    while time.time() < deadline:
        app.processEvents()
        main_frame = browser.web.page().mainFrame()
        matches = main_frame.findAllElements(pattern)
        if matches and not seg_botao_found:
            for m in matches:
                if m.attribute("value") == value_2:
                    theSecButtonMatch = m
                    print 'Acho que achei o botao 2!'
                    seg_botao_found = True
        if matches and seg_botao_found:
            break

    if theSecButtonMatch is not None:
        print 'Beleza! Achei mesmo o botao 2!'
    else:
        print 'Ah, nao! Nao achei o botao 2!'

    theSecButtonMatch.evaluateJavaScript(js_click)

    deadline = time.time() + timeout

    href = u"https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=downLoad"
    href2 = u"../consultarvalores/consultarValoresSeries.do?method=downLoad"
    link_pattern = "a"
    link_match = None

    while time.time() < deadline:
        app.processEvents()
        main_frame = browser.web.page().currentFrame()
        matches = main_frame.findAllElements(link_pattern)
        if matches:
            for m in matches:
                if m.attribute("href") == href or m.attribute("href") == href2:
                    print 'Encontrou um dos links! 1'
                    link_match = m
        if link_match:
            break

    if link_match is not None:
        print 'Removendo atribute target!'
        link_match.removeAttribute("target")
        print 'atribute target removido!'
        print 'Beleza! Achei mesmo o link 1!'
        browser.web.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
        print 'habilitando o browser...!'
        link_match.evaluateJavaScript(js_click)
        print 'cliquei no link...!'
    else:
        print 'Ah, nao! Nao achei o link 1!'

    #https://stackoverflow.com/questions/11043807/pyside-qbrowser.web-and-downloading-unsupported-content
    
    app.exec_()

