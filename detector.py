
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

from dbus.mainloop.glib import DBusGMainLoop
try:
    from urllib.parse import unquote
except ImportError:
    from urlparse import unquote


class MountDetector(dbus.service.Object):

    MOUNT_SERVICE = 'org.gtk.Private.RemoteVolumeMonitor'
    MOUNT_NAME = 'com.newsages.Private.RemoteVolumeMonitor'
    MOUNT_NAME_PATH = '/com/newsages/Private/RemoteVolumeMonitor/object'

    # def __init__(self, mount_info=None):
    def __init__(self):
        """
        Create a dbus based monitor
        """
        self._create_session_bus()
        self._check_service()
        self._connect_signals()

        loop = gobject.MainLoop()
        loop.run()

    # Configure Object
    def _create_session_bus(self):
        dbus_loop = DBusGMainLoop(set_as_default=True)
        self._session_bus = dbus.SessionBus(mainloop=dbus_loop)    
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        dbus.service.Object.__init__(self, self._session_bus, self.MOUNT_NAME_PATH)
        # print 'Dbus services:', str(self._session_bus.list_names())

    def _connect_signals(self):
        self._session_bus.add_signal_receiver(
                                              self.MountAdded,
                                              'MountAdded',
                                              self.MOUNT_SERVICE
                                              )
        self._session_bus.add_signal_receiver(
                                              self.MountRemoved,
                                              'MountRemoved',
                                              self.MOUNT_SERVICE
                                              )
        print("Connected")

    def _check_service(self):
        self.service = dbus.service.BusName(
                                            self.MOUNT_NAME, 
                                            self._session_bus
                                            )

    #SIGNALS AND METHODS
    @dbus.service.signal(MOUNT_NAME)
    def UriMount(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    @dbus.service.method(MOUNT_NAME)
    def MountAdded(self, sender, mount_id, data):
        print("mount_added")
        mount_point = str(data[5].split('://')[1])
        print mount_point
        self.UriMount(mount_point)
        return 'Signal emitted'

    @dbus.service.signal(MOUNT_NAME)
    def UriUmount(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    @dbus.service.method(MOUNT_NAME)
    def MountRemoved(self, sender, mount_id, data):
        print ('mount removed')
        mount_point = str(data[5].split('://')[1])
        print mount_point
        self.UriUmount(mount_point)
        return 'Signal emitted'    

    def Exit(self):
        loop.quit()

if __name__ == '__main__':
    object = MountDetector()
