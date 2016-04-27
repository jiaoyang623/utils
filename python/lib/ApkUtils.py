# encoding=utf-8
import os
import sys


class ApkUtils:
    def __init__(self):
        return

    @staticmethod
    def setutf8():
        reload(sys)
        sys.setdefaultencoding('utf8')
        return

    @staticmethod
    def sign(keystore, storepass, keypass, alias, src, dst):
        cmd = 'jarsigner -verbose -digestalg SHA1 -sigalg MD5withRSA' \
              ' -keystore %s -storepass "%s"  -keypass "%s" -signedjar %s %s %s' \
              % (keystore, storepass, keypass, dst, src, alias)
        os.system(cmd)
        return

    @staticmethod
    def zipalign(src, dst):
        cmd = 'zipalign -v 4 %s %s' % (src, dst)
        os.system(cmd)
        return

    @staticmethod
    def sign_with_config(src, dst, config_path):
        config = ApkUtils.read_keystore_config(config_path)
        if 'key.store' in config:
            storepath = config['key.store']
            ApkUtils.sign(storepath, config['key.store.password'],
                          config['key.alias.password'], config['key.alias'], src, dst)
        return

    @staticmethod
    def read_keystore_config(path):
        with open(path) as f:
            content = f.read()
        if len(content) == 0:
            return
        lines = [i for i in content.split('\n') if '=' in i]
        result = {}
        for l in lines:
            c = l.split('=')
            result[c[0]] = c[1]
        storepath = result['key.store']
        if not os.path.exists(storepath):
            dirpath = os.path.dirname(os.path.abspath(path))
            storepath = dirpath + '/' + storepath
            print storepath
            result['key.store'] = storepath
        return result

    @staticmethod
    def jiagu(src, dst):
        cmd_path = sys.path[0] + '/lib/tools/jiagu.jar'
        dir_name = 'jiagu_tmp'
        if os.path.exists(dir_name):
            os.system('rm -rf %s' % dir_name)
        os.mkdir(dir_name)
        cmd = 'java -jar %s -jiagu %s %s' % (cmd_path, src, dir_name)
        os.system(cmd)
        if len(os.listdir(dir_name)):
            os.system('mv %s/* %s' % (dir_name, dst))
            os.removedirs(dir_name)
        return

    @staticmethod
    def jiagu_sign(src, dst, key_config):
        ApkUtils.jiagu(src, dst + '_jiagu.apk')
        ApkUtils.sign_with_config(dst + '_jiagu.apk', dst + '_signed.apk', key_config)
        ApkUtils.zipalign(dst + '_signed.apk', dst)
        os.remove(dst + '_jiagu.apk')
        os.remove(dst + '_signed.apk')

    @staticmethod
    def options(opts):
        config = src = dst = action = ''
        for op, value in opts:
            if '-c' == op:
                config = value
            elif '-s' == op:
                src = value
            elif '-d' == op:
                dst = value
            elif '-a' == op:
                action = value
        if config and src and dst and action == 'sign':
            ApkUtils.sign_with_config(src, dst, config)
        elif src and dst and action == 'zipalign':
            ApkUtils.zipalign(src, dst)
        elif src and dst and config and action == 'jiagu':
            ApkUtils.jiagu_sign(src, dst, config)
        return

# ApkUtils.jiagu_sign(
#     '/opt/jenkins/workspace/360Video_trunk/trunk/360Video/bin/360Video-release.apk',
#     '/home/guowei/Desktop/result.apk',
#     '/opt/zygote/360Video/tags/ant.properties.clone')
