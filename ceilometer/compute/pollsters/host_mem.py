import ceilometer
from ceilometer.compute import plugin
from ceilometer.compute.pollsters import util
from ceilometer.compute.virt import inspector as virt_inspector
from ceilometer.openstack.common.gettextutils import _
from ceilometer.openstack.common import log
from ceilometer import sample
from collections import OrderedDict
import os

LOG = log.getLogger(__name__)


class HOSTMEMUtilPollster(plugin.ComputePollster):

     def get_samples(self, manager, cache, resources):
        meminfo = OrderedDict()
        if os.path.isfile("/proc/meminfo"):
            with open("/proc/meminfo") as f:
                for line in f:
                    temp = line.split(":")
                    meminfo[temp[0]] = temp[1].strip()
            if (meminfo.has_key('MemTotal') and meminfo.has_key('MemFree')):
                memtotal = int(meminfo['MemTotal'].strip().split(' ')[0])
                memfree = int(meminfo['MemFree'].strip().split(' ')[0])
                memutil = (memtotal - memfree)/(1.0*memtotal)
                memutil = float("%.2f"%memutil)*100  
                
            hostinfo = os.popen("uname -a").read()
            host = hostinfo.split(' ')[1]         
            
            yield util.make_sample_from_host(
                host,
                name='host_mem_util',
                type=sample.TYPE_DELTA,
                unit='%',
                volume=memutil,
                additional_metadata=None,
            )
        else:
            LOG.error(" the /proc/meminfo is not exist")
            



