import gobject
import dbus #@UnusedImport
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from urllib.parse import unquote
import dbus.service
import traceback
import sys
import os
from urllib.parse import unquote


class MountDetector:
    """
    Detect mount events from dbus session.
    
    Example of event fired on dbus:
    
    signal sender=:1.37 -> dest=(null destination) serial=131 path=/org/gtk/Private/RemoteVolumeMonitor; interface=org.gtk.Private.RemoteVolumeMonitor; member=MountRemoved
    string "org.gtk.Private.GduVolumeMonitor"
    string "0x9f7d940"
    struct {
       string "0x9f7d940"
       string "My Passport"
       string ". GThemedIcon drive-harddisk-usb drive-harddisk drive"
       string ""
       string "file:///media/My%20Passport"
       boolean true
       string ""
       array [
       ]
    }
    """
    
    MOUNT_SERVICE = 'org.gtk.Private.RemoteVolumeMonitor'
    
    def __init__(self, mount_info=None):
        """
        Create a dbus based monitor
        """
        self.mount_info = None
        
        if mount_info:
            self.mount_info = mount_info
                
        self._create_session_bus()
        self._check_service()
        self._connect_signals()

        loop = gobject.MainLoop()
        loop.run()
   
    def _create_session_bus(self):
        
        # Setting the DBusGMainLoop as default which allows to receive DBus 
        # calls during the gtk.main loop
        dbus_loop = DBusGMainLoop(set_as_default = True)
        
        self._session_bus = dbus.SessionBus(mainloop = dbus_loop)
        #print 'Dbus services:', str(self._session_bus.list_names())
   
    def _connect_signals(self):
        """
        This code could be replaced by gio.VolumeMonitor that is actually a high
        level abstraction for dbus mount signals. But for the purpose of the
        application use only a couple of calls of dbus is more useful.
        
        from gio import VolumeMonitor
        self._volume_monitor = VolumeMonitor()
        self._volume_monitor.connect('mount-added', self._add_mount)
        self._volume_monitor.connect('mount-removed', self._remove_mount)
        """
        
        # connect dbus signals
        self._session_bus.add_signal_receiver(
                                              self._mount_added,
                                              'MountAdded',
                                              self.MOUNT_SERVICE
                                              )
        self._session_bus.add_signal_receiver(
                                             self._mount_removed,
                                             'MountRemoved',
                                             self.MOUNT_SERVICE
                                            )
        print("Connected")
   
    def _check_service(self):
        service = dbus.service.BusName(self.MOUNT_SERVICE, self._session_bus) 
        
        
    def _mount_added(self, sender, mount_id, data):
    	print("mount_added")
    	disk_name = unquote(data[4][7:]) # Remove chars like %20 or similar
    	print (disk_name)
        
        # """
        # Handle adding of new device
        
        # Using gio.VolumeMonitor result as:
        
        # def _add_mount(self, monitor, mount):
        #     icon_names = mount.get_icon().to_string()
        #     print icon_names
        #     print mount.get_name()
        #     print mount.get_root()
        #     print mount.get_root().get_path()
        #     print mount
        #     print monitor
        # """

        # Another parse way: data[4].split('://')[1]
        
       
        # disk = os.statvfs(disk_name)
        
        # print ("preferred block size", "=>", disk.f_bsize)
        # print ("fundamental block size", "=>", disk.f_frsize)
        # print ("total blocks", "=>", disk.f_blocks)
        # print ("total free blocks", "=>", disk.f_bfree)
        # print ("available blocks", "=>", disk.f_bavail)
        # print ("total file nodes", "=>", disk.f_files)
        # print ("total free nodes", "=>", disk.f_ffree)
        # print ("available nodes", "=>", disk.f_favail)
        # print ("max file name length", "=>", disk.f_namemax)
        
        # totalSize = (disk.f_bsize * disk.f_bfree)
        # print (totalSize) # Size MB
        # print (self.convert_bytes(totalSize))
        
        # capacity = disk.f_bsize * disk.f_blocks
        # print (self.convert_bytes(capacity))
        
        # # Available bytes = Prefererred block zize * Available blocks
        # available = disk.f_bsize * disk.f_bavail
        # print (self.convert_bytes(available))
        
        # # Used bytes = Prefererred block zize * (Total blocks - Available blocks)
        # # used = disk.f_bsize * (disk.f_blocks - disk.f_bavail)
        # # print self.convert_bytes(used)
        
        # #label = data[1]
        # #icon = self._application.icon_manager.get_mount_icon_name(data[2])
        # #mount_point = data[4].split('://')[1]

        # #self._add_item(label, mount_point, mount_id, icon)
        
        # # Storage: My Passort 16GB/450 GB available
        # if self.mount_info:
        #     self.progress_bar_text.set_label('Storage: ' + os.path.basename(disk_name) + '    ' + self.convert_bytes(totalSize) + '/' + self.convert_bytes(capacity) + ' available')
        #     self.progress_bar.set_fraction(totalSize / float(capacity))
        #     self.progress_bar.set_text(self.convert_bytes(totalSize) + '/' + self.convert_bytes(capacity))

    def _mount_removed(self, sender, mount_id, data):
        """Handle removal of device"""
        
        print ('mount removed')
        
        # if self.mount_info:
        #     self.progress_bar_text.set_label('Storage: device no detected')
        #     self.progress_bar.set_fraction(0)
        #     self.progress_bar.set_text('-')
        
        # print (data)
        # #mount_point = data[4].split('://')[1]
        #self._remove_item(mount_point)

    def convert_bytes(self, bytes): #@ReservedAssignment
        '''
        
        @param bytes:
        '''
        bytes = float(bytes) #@ReservedAssignment
        if bytes >= 1099511627776:
            terabytes = bytes / 1099511627776
            size = '%.2f TiB' % terabytes
        elif bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2f GiB' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.2f MiB' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.2f KiB' % kilobytes
        else:
            size = '%.2f B' % bytes
        return size

MountDetector()