#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time
from subprocess import CalledProcessError, check_call, getstatusoutput, check_output
import json
import unittest
from pprint import pprint
from launcher_utils import *
from glob import glob
import dogtail.config

dogtail.config.config.logDebugToStdOut = False
dogtail.config.config.logDebugToFile = False

class DeepinAppstore:
    def __init__(self):
        self.appjson_cmd = 'lastore-tools update -j applications'
        self.appinstall_cmd = 'lastore-tools test -j install '
        self.appremove_cmd = 'lastore-tools test -j remove '
        #self.appremove_cmd = 'sudo apt-get -y remove '
    #'''
    def getdeblist(self):
        applist = getoutput(self.appjson_cmd)
        jsonstyle = json.loads(applist)
        #pprint(jsonstyle)
        debs = list(jsonstyle.keys())
        return debs
    '''
    def getdeblist(self):
        #return ['libreoffice','draftsight', 'deepin-screenshot', 'micropolis', 'gftp', 'brave']
        return ['gftp', 'libreoffice', 'deluge', 'wesnoth', 'gambas3', 'lazarus', 'glade', 'skype', 'monodevelop', 'firefox-dde', 'texmacs', 'eclipse-android',
                'nixnote2', 'qcad', 'freeciv', 'amarok', 'comix', 'scilab']
    #'''
appstore = DeepinAppstore()

def get_installed_apps():
    newInstalledApps = []
    debs = appstore.getdeblist()
    allApps = launcher.getAllApps()
    for deb in debs:
        for app in allApps:
            if deb in app.lower():
                newInstalledApps.append(deb)
                break
    return newInstalledApps

cutline = '-'*100 + '\n'


class TestAppstoreDebs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        updatefile = glob('/var/lib/dpkg/updates/*')
        lockfile = glob('/var/lib/dpkg/lock')
        cachefile = glob('/var/cache/apt/archives/lock')
        aptlock = glob('/var/lib/apt/lists/lock')
        if len(updatefile) > 0:
            check_call('sudo rm /var/lib/dpkg/updates/*', shell=True)
        if len(lockfile) > 0:
            check_call('sudo rm /var/lib/dpkg/lock', shell=True)
        if len(cachefile) > 0:
            check_call('sudo rm /var/cache/apt/archives/lock', shell=True)
        if len(aptlock) > 0:
            check_call('sudo rm /var/lib/apt/lists/lock', shell=True)
        cls.cutline = '-'*100 + '\n'
        cls.debs = appstore.getdeblist()
        #print(cls.debs)
        len_debs = len(cls.debs)
        cls.defaultWins = getAllWindows()

        cls.install_passed_apps = []
        cls.install_failed_apps = []
        cls.existed_apps = []

        cls.open_passed_apps = []
        cls.open_failed_apps = []

        cls.remove_passed_apps = []
        cls.remove_failed_apps = []
        cls.startTime = time.ctime()
        cls.stime = time.time()
        try:
            with open('apps.info', 'w') as f:
                print('The following %d debs in appstore will be checked:\n' % len_debs)
                f.write('The following %d debs in appstore will be checked:\n' % len_debs)
                for deb in cls.debs:
                    print('%s' % deb)
                    f.write('%s\n' % deb)
                print(cls.cutline)
                f.write(cls.cutline)
        except Exception as e:
            print(e)
        finally:
            f.close()
        closeWindows()

    @classmethod
    def tearDownClass(cls):
        cls.endTime = time.ctime()
        cls.etime = time.time()
        try:
            with open('apps.info', 'a') as f:
                f.write(cutline)
                print(cutline)

                f.write('install %d app%s passed:\n' % (len(self.install_passed_apps), len(self.install_passed_apps) > 1 and "s" or ""))
                print('install %d app%s passed:' % (len(self.install_passed_apps), len(self.install_passed_apps) > 1 and "s" or ""))
                if len(self.install_passed_apps) > 0:
                    f.write(','.join(self.install_passed_apps) + '\n\n')
                    print(self.install_passed_apps)
                    print('\n')
                f.write('install %d app%s failed:\n' % (len(self.install_failed_apps), len(self.install_failed_apps) > 1 and "s" or ""))
                print('install %d app%s failed:' % (len(self.install_failed_apps), len(self.install_failed_apps) > 1 and "s" or ""))
                if len(self.install_failed_apps) > 0:
                    f.write(','.join(self.install_failed_apps) + '\n\n')
                    print(self.install_failed_apps)
                    print('\n')
                f.write('%d app%s existed:\n' % (len(self.existed_apps), len(self.existed_apps) > 1 and "s" or ""))
                print('%d app%s existed:' % (len(self.existed_apps), len(self.existed_apps) > 1 and "s" or ""))
                if len(self.existed_apps) > 0:
                    f.write(','.join(self.existed_apps) + '\n\n')
                    print(self.existed_apps)
                    print('\n')
                f.write(cutline)
                print(cutline)

                f.write('open %d app%s passed:\n' % (len(self.open_passed_apps), len(self.open_passed_apps) > 1 and "s" or ""))
                print('open %d app%s passed:' % (len(self.open_passed_apps), len(self.open_passed_apps) > 1 and "s" or ""))
                if len(self.open_passed_apps) > 0:
                    f.write(','.join(self.open_passed_apps) + '\n\n')
                    print(self.open_passed_apps)
                    print('\n')
                f.write('open %d app%s failed:\n' % (len(self.open_failed_apps), len(self.open_failed_apps) > 1 and "s" or ""))
                print('open %d app%s failed:' % (len(self.open_failed_apps), len(self.open_failed_apps) > 1 and "s" or ""))
                if len(self.open_failed_apps) >0:
                    f.write(','.join(self.open_failed_apps) + '\n\n')
                    print(self.open_failed_apps)
                    print('\n')
                f.write(cutline)
                print(cutline)

                f.write('remove %d app%s passed:\n' % (len(self.remove_passed_apps), len(self.remove_passed_apps) > 1 and "s" or ""))
                print('remove %d app%s passed:' % (len(self.remove_passed_apps), len(self.remove_passed_apps) > 1 and "s" or ""))
                if len(self.remove_passed_apps) > 0:
                    f.write(','.join(self.remove_passed_apps) + '\n\n')
                    print(self.remove_passed_apps)
                    print('\n')
                f.write('remove %d app%s failed:\n' % (len(self.remove_failed_apps), len(self.remove_failed_apps) > 1 and "s" or ""))
                print('remove %d app%s failed:' % (len(self.remove_failed_apps), len(self.remove_failed_apps) > 1 and "s" or ""))
                if len(self.remove_failed_apps) > 0:
                    f.write(','.join(self.remove_failed_apps) + '\n\n')
                    print(self.remove_failed_apps)
                    print('\n')
                f.write(cutline)
                print(cutline)
                f.write('Start time: %s\n' % cls.startTime)
                f.write('End time  : %s\n' % cls.endTime)
                print('Start time: %s' % cls.startTime)
                print('End time  : %s' % cls.endTime)
                time_taken = float(cls.etime) - float(cls.stime)
                m, s = divmod(time_taken, 60)
                h, m = divmod(m, 60)
                print('Total used: %02dH:%02dM:%02dS' % (h, m, s))
                f.write('Total used: %02dH:%02dM:%02dS\n' % (h, m, s))
        except Exception as e:
            print(e)
        finally:
            f.close()
        cls.wins = getAllWindows()
        if len(cls.wins) > len(cls.defaultWins):
            for win in cls.wins[len(cls.defaultWins):]:
                win.close(1)

    def setUp(self):
        self.defaultWins = getAllWindows()
        closeWindows()

    def tearDown(self):
        self.wins = getAllWindows()
        if len(self.wins) > len(self.defaultWins):
            for win in self.wins[len(self.defaultWins):]:
                win.close(1)
    @property
    def install_passed_apps(self):
        return self.install_passed_apps

    @property
    def install_failed_apps(self):
        return self.install_failed_apps

    @property
    def existed_apps(self):
        return self.existed_apps

    @property
    def open_passed_apps(self):
        return self.open_passed_apps

    @property
    def open_failed_apps(self):
        return self.open_failed_apps

    @property
    def remove_passed_apps(self):
        return self.remove_passed_apps

    @property
    def remove_failed_apps(self):
        return self.remove_failed_apps


    def test_debs(self):
        debs = self.debs
        defaultwins = getAllWindows()
        with open('apps.info', 'a') as f:
            f.write('test install open remove deb\n')
            f.write(cutline)
            print('\033[1;31m%s\033[0m' % 'test install open remove deb')
            print(cutline)

            for deb in debs:

                #install
                install_deb(f, deb)
                #t1 = threading.Thread(target=install_deb, args=(f,deb))
                #t1.setDaemon(True)
                #t1.start()

                #open
                open_app(f, deb)

                #remove
                remove_deb(f, deb)
            '''
            f.write(cutline)
            print(cutline)

            f.write('install %d app%s passed:\n' % (len(self.install_passed_apps), len(self.install_passed_apps) > 1 and "s" or ""))
            print('install %d app%s passed:' % (len(self.install_passed_apps), len(self.install_passed_apps) > 1 and "s" or ""))
            if len(self.install_passed_apps) > 0:
                f.write(','.join(self.install_passed_apps) + '\n\n')
                print(self.install_passed_apps)
                print('\n')
            f.write('install %d app%s failed:\n' % (len(self.install_failed_apps), len(self.install_failed_apps) > 1 and "s" or ""))
            print('install %d app%s failed:' % (len(self.install_failed_apps), len(self.install_failed_apps) > 1 and "s" or ""))
            if len(self.install_failed_apps) > 0:
                f.write(','.join(self.install_failed_apps) + '\n\n')
                print(self.install_failed_apps)
                print('\n')
            f.write('%d app%s existed:\n' % (len(self.existed_apps), len(self.existed_apps) > 1 and "s" or ""))
            print('%d app%s existed:' % (len(self.existed_apps), len(self.existed_apps) > 1 and "s" or ""))
            if len(self.existed_apps) > 0:
                f.write(','.join(self.existed_apps) + '\n\n')
                print(self.existed_apps)
                print('\n')
            f.write(cutline)
            print(cutline)

            f.write('open %d app%s passed:\n' % (len(self.open_passed_apps), len(self.open_passed_apps) > 1 and "s" or ""))
            print('open %d app%s passed:' % (len(self.open_passed_apps), len(self.open_passed_apps) > 1 and "s" or ""))
            if len(self.open_passed_apps) > 0:
                f.write(','.join(self.open_passed_apps) + '\n\n')
                print(self.open_passed_apps)
                print('\n')
            f.write('open %d app%s failed:\n' % (len(self.open_failed_apps), len(self.open_failed_apps) > 1 and "s" or ""))
            print('open %d app%s failed:' % (len(self.open_failed_apps), len(self.open_failed_apps) > 1 and "s" or ""))
            if len(self.open_failed_apps) >0:
                f.write(','.join(self.open_failed_apps) + '\n\n')
                print(self.open_failed_apps)
                print('\n')
            f.write(cutline)
            print(cutline)

            f.write('remove %d app%s passed:\n' % (len(self.remove_passed_apps), len(self.remove_passed_apps) > 1 and "s" or ""))
            print('remove %d app%s passed:' % (len(self.remove_passed_apps), len(self.remove_passed_apps) > 1 and "s" or ""))
            if len(self.remove_passed_apps) > 0:
                f.write(','.join(self.remove_passed_apps) + '\n\n')
                print(self.remove_passed_apps)
                print('\n')
            f.write('remove %d app%s failed:\n' % (len(self.remove_failed_apps), len(self.remove_failed_apps) > 1 and "s" or ""))
            print('remove %d app%s failed:' % (len(self.remove_failed_apps), len(self.remove_failed_apps) > 1 and "s" or ""))
            if len(self.remove_failed_apps) > 0:
                f.write(','.join(self.remove_failed_apps) + '\n\n')
                print(self.remove_failed_apps)
                print('\n')
            f.write(cutline)
            print(cutline)
        '''
        #f.close()

debs = TestAppstoreDebs()

def closeWindows():
    newWins = getAllWindows()
    for win in newWins[len(debs.defaultWins):]:
        win.close(1)

def install_deb(f, deb):
    closeWindows()
    if deb == 'draftsight' or deb == 'micropolis':
        f.write('draftsight or micropolis will not to be installed\n')
        print('draftsight or micropolis will not to be installed')
        debs.install_failed_apps.append(deb)
        return
    try:
        output = check_output([appstore.appinstall_cmd + deb], shell=True, timeout=1800).decode()
    except CalledProcessError as e:
        output = e.output.decode()
        returncode = e.returncode
        if 'resource exists' in output:
            debs.existed_apps.append(deb)
            f.write(deb + ' existed:\n' + output + '\n\n' + cutline)
            print(deb + ' existed:\n' + output + '\n' + cutline)
        else:
            debs.install_failed_apps.append(deb)
            f.write('install ' + deb + ' failed:\n' + output + '\n\n' + cutline)
            print('install ' + deb + ' failed:\n' + output + '\n' + cutline)
    else:
        debs.install_passed_apps.append(deb)
        f.write('install ' + deb + ' successfully\n\n')
        print('install ' + deb + ' successfully\n')
    closeWindows()

def open_app(f, deb):
    closeWindows()
    launcher.searchApp(deb)
    sleep(1)
    serchresult = launcher.launcherObj.child('all',roleName='list').children
    s,o = getstatusoutput("apt-cache policy libreoffice |awk NR==2'{print $1}'")
    if len(serchresult) > 0:
        f.write('search %s result: %s\n' % (deb, serchresult[0].name))
        print('search %s result: %s' % (deb, serchresult[0].name))
        '''
        if (deb != 'libreoffice' and o == '已安装：(无)' and serchresult[0].name == 'LibreOffice') or (deb != 'deepin-wm' and serchresult[0].name == '多任务视图'):
            debs.open_failed_apps.append(deb)
            print("launcher not found %s but found %s" % (deb, serchresult[0].name))
            f.write("launcher not found %s but found %s\n\n" % (deb, serchresult[0].name))
            return
        '''
        pyautogui.press('enter')
        if deb == 'deepin-screenshot':
            sleep(5)
            status,output = getstatusoutput('ps aux |grep deepin-screenshot |grep -v grep')
            if status == 0:
                pyautogui.press('esc')
                debs.open_passed_apps.append(deb)
                f.write('opened ' + deb + ' successfully!\n\n')
                print('opened ' + deb + ' successfully!\n')
            else:
                debs.open_failed_apps.append(deb)
                f.write('opened ' + deb + ' failed!\n\n')
                print('opened ' + deb + ' failed!\n')
        else:
            if 'idea' in deb:
                sleep(12)
            else:
                sleep(5)
            newWins = getAllWindows()
            if len(newWins) > len(debs.defaultWins):
                debs.open_passed_apps.append(deb)
                f.write('opened ' + deb + ' successfully!\n\n')
                print('opened ' + deb + ' successfully!\n')
                for win in newWins[len(debs.defaultWins):]:
                    win.close(1)
            else:
                debs.open_failed_apps.append(deb)
                f.write('opened ' + deb + ' failed!\n\n')
                print('opened ' + deb + ' failed!\n')
            try:
                debs.assertGreater(newWins, debs.defaultWins, '%s was not opened successfully in launcher' % deb)
            except Exception as e:
                print(e)
        if serchresult[0].name == '多任务视图':
            pyautogui.press('esc')
    else:
        debs.open_failed_apps.append(deb)
        f.write("launcher not found %s \n\n" % deb)
        print("launcher not found %s " % deb)
        launcher.exitLauncher()

    closeWindows()

def remove_deb(f, deb):
    closeWindows()
    #status,output = getstatusoutput(appstore.appremove_cmd + deb)
    try:
        output = check_output([appstore.appremove_cmd + deb], shell=True, timeout=1800).decode()
    except CalledProcessError as e:
        output = e.output.decode()
        returncode = e.returncode
        debs.remove_failed_apps.append(deb)
        f.write('remove ' + deb + ' failed:\n' + output + '\n\n' + cutline)
        print('remove ' + deb + ' failed:\n' + output + '\n' + cutline)
    else:
        debs.remove_passed_apps.append(deb)
        f.write('remove ' + deb + ' successfully\n\n')
        print('remove ' + deb + ' successfully\n')

    if  deb == 'deepin-screenshot':
        pyautogui.press('esc')
    try:
        if deb == 'libreoffice':
            libreoffice_debs = ['libreoffice-common', 'libreoffice-calc', 'libreoffice-draw', 'libreoffice-impress',
                                'libreoffice-writer', 'libreoffice-base', 'libreoffice-math', 'openjdk-8-jre']
            for libreoffice_deb in libreoffice_debs:
                check_output([appstore.appremove_cmd + libreoffice_deb], shell=True, timeout=1800).decode()
        if deb == 'gftp':
            output = check_output([appstore.appremove_cmd + 'gftp-gtk'], shell=True, timeout=1800).decode()
            #check_call(appstore.appremove_cmd + 'gftp-gtk', shell=True)
        if deb == 'deluge':
            check_output([appstore.appremove_cmd + 'deluge-gtk'], shell=True, timeout=1800).decode()
        if deb == 'wesnoth':
            check_output([appstore.appremove_cmd + 'wesnoth-1.12-core'], shell=True, timeout=1800).decode()
        if deb == 'gambas3':
            check_output([appstore.appremove_cmd + 'gambas3-ide'], shell=True, timeout=1800).decode()
        if deb == 'lazarus':
            check_output([appstore.appremove_cmd + 'lazarus-ide-1.6'], shell=True, timeout=1800).decode()
        if deb == 'glade':
            check_output([appstore.appremove_cmd + 'devhelp'], shell=True, timeout=1800).decode()
        if deb == 'skype':
            check_output([appstore.appremove_cmd + 'skype-bin'], shell=True, timeout=1800).decode()
        if deb == 'monodevelop':
            check_output([appstore.appremove_cmd + 'monodoc-browser'], shell=True, timeout=1800).decode()
        if deb == 'firefox-dde':
            check_output([appstore.appremove_cmd + 'firefox'], shell=True, timeout=1800).decode()
        if deb == 'texmacs':
            check_output([appstore.appremove_cmd + 'xfig'], shell=True, timeout=1800).decode()
        ''''
        if deb == 'eclipse-android' or deb == 'myeclipse' or deb == 'minecraft' or deb == 'eclipse-jee' or deb == 'eclipse-committers'
            or deb == 'smartsvn' or deb == 'smartcvs' or deb == 'magarena' or deb == 'freecol' or deb == 'eclipse-cpp' or deb == 'eclipse-rcp'
            or deb == 'eclipse-java' or deb == 'eclipse-javascript' or deb == 'eclipse-testing' or deb == 'eclipse-scout' or deb == 'eclipse-reporting':
        '''
        if 'eclipse' in deb or deb == 'smartsvn' or deb == 'smartcvs' or deb == 'magarena' or deb == 'freecol':
            check_output([appstore.appremove_cmd + 'openjdk-8-jre'], shell=True, timeout=1800).decode()
        if deb == 'gkdebconf' or deb == 'codelite' or deb == 'qtcreator' or deb == 'codeblocks':
            check_output([appstore.appremove_cmd + 'xterm'], shell=True, timeout=1800).decode()
        #if deb == 'lives' or deb == 'chromium' or deb == 'texmacs' or deb == 'playonlinux':
        #    check_call(appstore.appremove_cmd + '', shell=True)
        if deb == 'qcad':
            check_output([appstore.appremove_cmd + 'qjackctl'], shell=True, timeout=1800).decode()
        if deb == 'freeciv':
            freeciv_debs = ['freeciv-server', 'freeciv-client-gtk']
            for freeciv_deb in freeciv_debs:
                check_output([appstore.appremove_cmd + freeciv_deb], shell=True, timeout=1800).decode()
        if deb == 'amarok':
            check_output([appstore.appremove_cmd + 'amarok-utils'], shell=True, timeout=1800).decode()
        if deb == 'comix':
            check_output([appstore.appremove_cmd + 'mcomix'], shell=True, timeout=1800).decode()
        if deb == 'scilab':
            check_output([appstore.appremove_cmd + 'scilab-cli'], shell=True, timeout=1800).decode()
        if deb == 'nixnote2':
            check_output([appstore.appremove_cmd + 'libreoffice-common'], shell=True, timeout=1800).decode()
        if deb == 'vmpk':
            vmpk_debs = ['qjackctl', 'qsynth']
            for vmpk_deb in vmpk_debs:
                check_output([appstore.appremove_cmd + vmpk_deb], shell=True, timeout=1800).decode()
    except Exception as e:
        print(e)
    closeWindows()

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(TestAppstoreDebs('test_install_debs'))
    #suite.addTest(TestAppstoreDebs('test_open_apps'))
    #suite.addTest(TestAppstoreDebs('test_remove_debs'))
    suite.addTest(TestAppstoreDebs('test_debs'))
    return suite

alltests = unittest.TestSuite(suite())

if __name__ == '__main__':
    with open('test.result', 'w') as logf:
        unittest.TextTestRunner(stream=logf,verbosity=2).run(alltests)
    logf.close()
