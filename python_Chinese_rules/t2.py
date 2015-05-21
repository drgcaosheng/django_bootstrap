#!/usr/bin/env python
# encoding: utf-8
# 如果觉得不错，可以推荐给你的朋友！http://tool.lu/pyc
import sys
import os
import time
import json
import signal
import gevent
from gevent.server import StreamServer
from gevent.monkey import patch_socket
patch_socket()
import lib.Common as Common
_DEBUG = False
_cache_data = { }
_cache_life = 30

class Processor(object):
    
    def __init__(self, ident, query_list):
        self.ident = ident
        self.query_list = query_list

    
    def run(self):
        data = [
            'RESULT']
        for query in self.query_list:
            
            try:
                (flag, path, qtype) = query.split('::')
                cache_key = '%s::%s' % (path, qtype)
                size_data = self._get_data_from_cache(cache_key)
                if size_data is not None:
                    loginfo(self.ident, 'cache: <%s>' % cache_key)
                else:
                    loginfo(self.ident, ' stat: <%s>' % cache_key)
                    size_data = self._stat_mailbox_size(path, qtype)
                    if size_data is not None:
                        self._save_data_to_cache(cache_key, size_data)
            except:
                logerror(self.ident, 'query param error: %s' % query)
                continue

            data.append('%s::%s' % (flag, size_data))
        
        data.append('.\n')
        return data

    
    def _get_data_from_cache(key):
        size = None
        if key in _cache_data and isinstance(_cache_data[key], tuple):
            size = _cache_data[key][0]
        return size

    _get_data_from_cache = staticmethod(_get_data_from_cache)
    
    def _save_data_to_cache(key, val):
        _cache_data[key] = (val, time.time())

    _save_data_to_cache = staticmethod(_save_data_to_cache)
    
    def _stat_mailbox_size(self, path, qtype):
        mbox_path = '%s/%s' % (Common.MAILBOX_ROOT, path)
        if not os.path.isdir(mbox_path):
            logerror(self.ident, 'not found mailbox path')
            return None
        if None == 'folder':
            size_data = self._stat_folder_list_size(mbox_path)
            return size_data
        if None == 'all':
            size_stat = self._stat_folder_size(mbox_path)
            return str(size_stat)

    
    def _stat_folder_list_size(self, mbox_path):
        size_total = 0x0L
        size_inbox = 0x0L
        size_folder = { }
        for real_name in os.listdir(mbox_path):
            if real_name in ('cur', 'new'):
                size_inbox += self._stat_folder_size(mbox_path + real_name)
                continue
            if real_name[0:1] == '.':
                s = self._stat_folder_size(mbox_path + real_name)
                size_folder[real_name[1:]] = s
                size_total += s
                continue
        size_total += size_inbox
        size_folder['inbox'] = size_inbox
        return json.dumps({
            'total': size_total,
            'folder': size_folder })

    
    def _stat_folder_size(self, folder):
        gevent.sleep(0)
        size = 0x0L
        for (root, dirs, files) in os.walk(folder):
            for name in files:
                if name[0:7] == 'dovecot':
                    continue
                if name in ('subscriptions', 'maildirfolder'):
                    continue
                size += self._get_file_size(root + '/' + name)
            
        
        return size

    
    def _get_file_size(self, path):
        
        try:
            _size = os.path.getsize(path)
        except:
            _size = 0
            logerror(self.ident, 'stat file size exception: %s' % path)

        return _size



def cache_cleaner():
    
    def _cleanner():
        
        try:
            currtime = time.time()
            for (k, v) in _cache_data.items():
                if currtime - v[1] > _cache_life:
                    _cache_data.pop(k)
                    continue
        except:
            Common.outerror(Common.get_exception_info())


    while True:
        _cleanner()
        gevent.sleep(1)


def receive_client_query(file_object):
    query_list = []
    while True:
        gevent.sleep(0)
        line = file_object.readline()
        line = line.strip()
        if line == '.':
            break
        if not line:
            break
        query_list.append(line)
    if query_list[0] != 'QUERY':
        answer_data = 'invalid_command\n'
        file_object.write(answer_data)
        file_object.flush()
        gevent.sleep(0)
        return None
    None.pop(0)
    return query_list


def answer_query(file_object, data):
    file_object.write('\n'.join(data))
    file_object.flush()
    gevent.sleep(0)


def main(client_socket, address):
    ident = Common.get_random_string(10)
    file_object = client_socket.makefile()
    query_list = receive_client_query(file_object)
    if query_list is None:
        return None
    p = None(ident, query_list)
    data = p.run()
    answer_query(file_object, data)


def signal_handle(mode):
    Common.outinfo('catch signal: %s' % mode)
    if mode != 'sigint':
        sys.exit(0)


def loginfo(logid, msg):
    msg = u'[%s] %s' % (Common.get_unicode(logid), Common.get_unicode(msg))
    Common.outinfo(msg)


def logerror(logid, msg):
    msg = u'[%s] %s' % (Common.get_unicode(logid), Common.get_unicode(msg))
    Common.outerror(msg)

if __name__ == '__main__':
    globals()['_DEBUG'] = Common.check_debug()
    Common.init_run_user()
    Common.init_pid_file('sizequerier.pid')
    Common.init_logger('SizeQuerier', len(sys.argv) > 1, _DEBUG)
    Common.Core.check_initialization()
    Common.init_cfg_default()
    EXIT_CODE = 0
    Common.outinfo('program start')
    
    try:
        gevent.signal(signal.SIGTERM, signal_handle, 'sigterm')
        gevent.signal(signal.SIGALRM, signal_handle, 'sigalrm')
        gevent.spawn(cache_cleaner)
        server = StreamServer(('127.0.0.1', 10029), main)
        server.serve_forever()
    except KeyboardInterrupt:
        signal_handle('sigint')
    except SystemExit:
        e = None
        EXIT_CODE = e.code
    except:
        Common.outerror(Common.get_exception_info())
        EXIT_CODE = 1

    Common.outinfo('program quit')
    sys.exit(EXIT_CODE)
