import ceilometer
from ceilometer.compute import plugin
from ceilometer.compute.pollsters import util
from ceilometer.compute.virt import inspector as virt_inspector
from ceilometer.openstack.common.gettextutils import _
from ceilometer.openstack.common import log
from ceilometer import sample
import os
import util
import statvfs
from collections import OrderedDict


LOG = log.getLogger(__name__)


class HOSTDISKUtilPollster(plugin.ComputePollster):

    def get_samples(self, manager, cache, resources):
        diskinfo = os.statvfs("/")
        available = diskinfo[statvfs.F_BAVAIL]/1024.0*diskinfo[statvfs.F_BSIZE]/(1024.0*1024)
        capacity = diskinfo[statvfs.F_BLOCKS]/1024.0*diskinfo[statvfs.F_BSIZE]/(1024.0*1024)
        diskutil = (capacity - available)*1.0 / capacity       
        diskutil = float("%.2f"%diskutil) * 100    
        hostinfo = os.popen("uname -a").read()
        host = hostinfo.split(' ')[1]   
        
        yield util.make_sample_from_host(
            host,
            name='host_disk_util',
            type=sample.TYPE_DELTA,
            unit='%',
            volume=diskutil,
            additional_metadata=None,
        )
            

