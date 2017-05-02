import time,datetime
import xbmc
import xbmcaddon

from datetime import date, timedelta

ADDON = xbmcaddon.Addon(id='plugin.video.imdb.tv')

def subscription_update():
    if ADDON.getSetting('subscription_update') == "true":
        return True
    else:
        return False

def update_tv():
    if ADDON.getSetting('update_tv') == "true":
        return True
    else:
        return False

def update_TV():
    if ADDON.getSetting('update_TV') == "true":
        return True
    else:
        return False

def subscription_timer():
    return int(ADDON.getSetting('subscription_timer'))

class AutoUpdater:
    def update(self):
        hours_list = [2, 5, 10, 15, 24]
        hours = hours_list[subscription_timer()]
        xbmc.log('[IMDb TV] Updating', level=xbmc.LOGNOTICE)
        time.sleep(1)
        if update_TV():
            xbmc.log('[IMDb TV] Updating TV', level=xbmc.LOGNOTICE)
            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.imdb.tv/update_TV)')
        if update_tv():
            xbmc.log('[IMDb TV] Updating TV Shows', level=xbmc.LOGNOTICE)
            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.imdb.tv/update_tv)')
        now = datetime.datetime.now()
        ADDON.setSetting('service_time', str(now + timedelta(hours=hours)).split('.')[0])
        xbmc.log("[IMDb TV] Library updated. Next run at " + ADDON.getSetting('service_time'), level=xbmc.LOGNOTICE)
        if ADDON.getSetting('update_main') == "true":
            while (xbmc.getCondVisibility('Library.IsScanningVideo') == True):
                time.sleep(1)
                if xbmc.abortRequested:
                    return
            xbmc.log('[IMDb TV] Updating Kodi Library', level=xbmc.LOGNOTICE)
            xbmc.executebuiltin('UpdateLibrary(video)')
        if ADDON.getSetting('update_clean') == "true":
            time.sleep(1)
            while (xbmc.getCondVisibility('Library.IsScanningVideo') == True):
                time.sleep(1)
                if xbmc.abortRequested:
                    return
            xbmc.log('[IMDb TV] Cleaning Kodi Library', level=xbmc.LOGNOTICE)
            xbmc.executebuiltin('CleanLibrary(video)')

    def runProgram(self):
        if ADDON.getSetting('login_update') == "true":
            delay = int(ADDON.getSetting('login_delay'))
            time.sleep(delay*60)
            self.update()
        while not xbmc.abortRequested:
            if subscription_update():
                try:
                    next_run  = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ADDON.getSetting('service_time').encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
                    now = datetime.datetime.now()
                    if now > next_run:
                        self.update()
                except Exception as detail:
                    xbmc.log("[IMDb TV] Update Exception %s" % detail, level=xbmc.LOGERROR)
                    pass
            time.sleep(1)


xbmc.log("[IMDb TV] Subscription service starting...", level=xbmc.LOGNOTICE)
AutoUpdater().runProgram()
