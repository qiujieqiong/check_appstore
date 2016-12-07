#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pyautogui
from dogtail.tree import *
import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import dbus
from time import sleep
from subprocess import getoutput
import json
from pprint import pprint
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1

def getAllWindows():
    try:
        wins = []
        screen = Wnck.Screen.get_default()
        screen.force_update()
        for win in screen.get_windows():
            wins.append(win)
        return wins
    finally:
        win = None
        screen = None
        Wnck.shutdown()


def getAllWindowNames():
    sleep(5)
    try:
        winNames = []
        screen = Wnck.Screen.get_default()
        screen.force_update()
        for win in screen.get_windows():
            winNames.append(win.get_name())
        return winNames
    finally:
        win = None
        screen = None
        Wnck.shutdown()

class Launcher:

    def __init__(self):
        self.launcherObj = root.application(appName='dde-launcher', description='/usr/bin/dde-launcher')
        self.menuObj = root.application(appName='deepin-menu', description='/usr/lib/deepin-menu')
        self.dbusDir = 'com.deepin.dde.daemon.Launcher'
        self.dbusObj = '/com/deepin/dde/daemon/Launcher'
        self.ifc = 'com.deepin.dde.daemon.Launcher'
        self.session_bus = dbus.SessionBus()
        self.session_obj = self.session_bus.get_object(self.dbusDir, self.dbusObj)
        self.session_if = dbus.Interface(self.session_obj,dbus_interface=self.ifc)

    def openLauncher(self):
        wins = getAllWindowNames()
        if 'dde-launcher' not in wins:
            pyautogui.press('winleft')
        else:
            pyautogui.press('esc')
            sleep(1)
            pyautogui.press('winleft')

    def exitLauncher(self):
        wins = getAllWindowNames()
        if 'dde-launcher' in wins:
            pyautogui.press('esc')

    def searchApp(self,char):
        self.openLauncher()
        wins = getAllWindowNames()
        if 'dde-launcher' in wins:
            self.launcherObj.child('search-edit').click()
            sleep(1)
            self.launcherObj.child('search-edit').text = char
        else:
            print('launcher did not opened')

    def getInstalledApps(self):
        appnames = []
        newInstalledApps = self.session_if.GetAllNewInstalledApps()
        for item in newInstalledApps:
            applist = item.split("'")
            appnames.append(''.join(applist))
        return appnames
    '''
    def getAllApps(self):
        desktopfiles = []
        appnames = []
        allApps = self.session_if.GetAllItemInfos()
        for appinfo in allApps:
            desktopfiles.append(appinfo[0])
        str_desktopfiles = ','.join(desktopfiles)
        desktopfiles = str_desktopfiles.split(',')
        print(list(desktopfiles))
        print(len(list(desktopfiles)))
        for item in list(desktopfiles):
            app = getoutput("cat " + item + " |grep ^Icon |head -1 |cut -d = -f 2")
            appnames.append(''.join(app))
        return appnames
    '''
    def getAllApps(self):
        dbus_appnames = []
        appnames = []
        allApps = self.session_if.GetAllItemInfos()
        for appinfo in allApps:
            dbus_appnames.append(appinfo[2])
        for item in dbus_appnames:
            applist = item.split("'")
            appnames.append(''.join(applist))
        return appnames

    def uninstallApp(self,app):
        self.searchApp(app)
        sleep(2)
        #self.launcherObj.child(app).click(3)
        serchresult = self.launcherObj.child('all',roleName='list').children
        print(serchresult[0].name)
        if (len(serchresult)) == 1:
            appname = ''.join(serchresult[0].name)
            print(appname)
            self.launcherObj.child(appname).click(3)
            if self.menuObj.children[0].name == 'DesktopMenu':
                for i in range(5):
                    pyautogui.press('down')
                    sleep(0.5)
                pyautogui.press('enter')
            else:
                raise Exception("launcher menu did not opened!")
            sleep(1)
            self.launcherObj.child('确定').click()
            self.exitLauncher()
        else:
            raise Exception("launcher not found %s " % app)

    def openApp(self, app):
        self.searchApp(app)
        sleep(2)
        #self.launcherObj.child(app).click(3)
        serchresult = self.launcherObj.child('all',roleName='list').children
        if len(serchresult) > 0:
            print('search %s result: %s' % (app, serchresult[0].name))
        sleep(2)
        if len(serchresult) > 0:
            pyautogui.press('enter')
            '''
            appname = ''.join(serchresult[0].name)
            self.launcherObj.child(appname).click(3)
            if len(self.menuObj.children) >  0:
                pyautogui.press('down')
                sleep(1)
                pyautogui.press('enter')
                sleep(1)
                self.exitLauncher()
            else:
                print("launcher menu did not opened!")
            '''
        else:
            print("launcher not found %s " % app)
            self.exitLauncher()

launcher = Launcher()

class DeepinAppstore:
    def __init__(self):
        self.appjson_cmd = 'lastore-tools update -j applications'
        self.appinstall_cmd = 'lastore-tools test -j install '
        self.appremove_cmd = 'lastore-tools test -j remove '
        #self.appremove_cmd = 'sudo apt-get -y remove '

    def getdeblist(self):
        applist =  getoutput(self.appjson_cmd)
        jsonstyle = json.loads(applist)
        #pprint(jsonstyle)
        debs = list(jsonstyle.keys())
        return debs

appstore = DeepinAppstore()

if __name__ == '__main__':
    '''
    allApps = launcher.getAllApps()
    print(allApps)
    print(len(allApps))
    '''
    debs = appstore.getdeblist()
    print(debs)
