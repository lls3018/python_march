#!/usr/bin/env python

import re
import os
import pwd
import time
import glob
import json
import shlex
import urllib
import urllib2
import hashlib
import tempfile
import subprocess
from functools import wraps


def retry(exception, tries=4, delay=3, backoff=2):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception as ex:
                    msg = "{0}, Retrying in {1} seconds...".format(ex, mdelay)
                    print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


def get_file_contents(file_path):
    with open(file_path) as f:
        data = f.read().rstrip('\n')
    return data


def run(command, retries=0, ignore_failures=False, globx=False):
    if isinstance(command, str):
        command = shlex.split(command)
    stderr = subprocess.PIPE
    stdout = subprocess.PIPE
    if globx:
        glob_command = []
        for arg in command:
            glob_command.append(glob.glob(arg))
        command = glob_command
    print('Running: {0}'.format(command))
    proc = subprocess.Popen(command, stdout=stdout, stderr=stderr)
    proc.aggr_stdout, proc.aggr_stderr = proc.communicate()
    if proc.returncode != 0:
        command_str = ' '.join(command)
        if retries:
            print('Failed running command: {0}. Retrying. '
                            '({1} left)'.format(command_str, retries))
            proc = run(command, retries - 1)
        elif not ignore_failures:
            msg = 'Failed running command: {0} ({1}).'.format(
                command_str, proc.aggr_stderr)
            raise RuntimeError(msg)
    return proc


def sudo(command, retries=0, globx=False, ignore_failures=False):
    if isinstance(command, str):
        command = shlex.split(command)
    command.insert(0, 'sudo')
    return run(command=command, globx=globx, retries=retries,
               ignore_failures=ignore_failures)


def sudo_write_to_file(contents, destination):
    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, 'w') as f:
        f.write(contents)
    return move(path, destination)


def mkdir(dir, use_sudo=True):
    if os.path.isdir(dir):
        return
    print('Creating Directory: {0}'.format(dir))
    cmd = ['mkdir', '-p', dir]
    if use_sudo:
        sudo(cmd)
    else:
        run(cmd)

def move(source, destination, rename_only=False):
    if rename_only:
        sudo(['mv', '-T', source, destination])
    else:
        copy(source, destination)
        remove(source)


def copy(source, destination):
    sudo(['cp', '-rp', source, destination])


def remove(path, ignore_failure=False):
    if os.path.exists(path):
        print('Removing {0}...'.format(path))
        sudo(['rm', '-rf', path], ignore_failures=ignore_failure)
    else:
        print('Path does not exist: {0}. Skipping...'
                        .format(path))


def install_python_package(source, venv=''):
    if venv:
        print('Installing {0} in virtualenv {1}...'.format(
            source, venv))
        sudo(['{0}/bin/pip'.format(
            venv), 'install', source, '--upgrade'])
    else:
        print('Installing {0}'.format(source))
        sudo(['pip', 'install', source, '--upgrade'])


def curl_download_with_retries(source, destination):
    curl_cmd = ['curl']
    curl_cmd.extend(['--retry', '10'])
    curl_cmd.append('--fail')
    curl_cmd.append('--silent')
    curl_cmd.append('--show-error')
    curl_cmd.extend(['--location', source])
    curl_cmd.append('--create-dir')
    curl_cmd.extend(['--output', destination])
    print('curling: {0}'.format(' '.join(curl_cmd)))
    run(curl_cmd)


def download_file(url, destination=''):
    if not destination:
        fd, destination = tempfile.mkstemp()
        os.remove(destination)
        os.close(fd)

    if not os.path.isfile(destination):
        print('Downloading {0} to {1}...'.format(url, destination))
        try:
            final_url = urllib.urlopen(url).geturl()
            if final_url != url:
                print('Redirected to {0}'.format(final_url))
            f = urllib.URLopener()
            # TODO: try except with @retry
            f.retrieve(final_url, destination)
        except:
            curl_download_with_retries(url, destination)
    else:
        print('File {0} already exists...'.format(destination))
    return destination


def get_file_name_from_url(url):
    try:
        return url.split('/')[-1]
    except:
        # in case of irregular url. precaution.
        # note that urlparse is deprecated in Python 3
        from urlparse import urlparse
        disassembled = urlparse(url)
        return os.path.basename(disassembled.path)

def yum_install(source, service_name):
    """Installs a package using yum.

    yum supports installing from URL, path and the default yum repo
    configured within your image.
    you can specify one of the following:
    [yum install -y] mylocalfile.rpm
    [yum install -y] mypackagename

    If the source is a package name, it will check whether it is already
    installed. If it is, it will do nothing. It not, it will install it.

    If the source is a url to an rpm and the file doesn't already exist
    in a predesignated archives file path (${CLOUDIFY_SOURCES_PATH}/),
    it will download it. It will then use that file to check if the
    package is already installed. If it is, it will do nothing. If not,
    it will install it.

    NOTE: This will currently not take into considerations situations
    in which a file was partially downloaded. If a file is partially
    downloaded, a redownload will not take place and rather an
    installation will be attempted, which will obviously fail since
    the rpm file is incomplete.
    ALSO NOTE: you cannot provide `yum_install` with a space
    separated array of packages as you can with `yum install`. You must
    provide one package per invocation.
    """
    # source is a url
    if source.startswith(('http', 'https', 'ftp')):
        filename = get_file_name_from_url(source)
        source_name, ext = os.path.splitext(filename)
    # source is just the name of the file
    elif source.endswith('.rpm'):
        source_name, ext = os.path.splitext(source)
    # source is the name of a yum-repo based package name
    else:
        source_name, ext = source, ''
    source_path = source_name

    if ext.endswith('.rpm'):
        source_path = download_file(source)

        rpm_handler = RpmPackageHandler(source_path)
        print('Checking whether {0} is already installed...'.format(
            source_path))
        if rpm_handler.is_rpm_installed():
            print('Package {0} is already installed.'.format(source))
            return

        # removes any existing versions of the package that do not match
        # the provided package source version
        rpm_handler.remove_existing_rpm_package()
    else:
        installed = run(['yum', '-q', 'list', 'installed', source_path],
                        ignore_failures=True)
        if installed.returncode == 0:
            print('Package {0} is already installed.'.format(source))
            return

    print('yum installing {0}...'.format(source_path))
    sudo(['yum', 'install', '-y', source_path])


class RpmPackageHandler(object):

    def __init__(self, source_path):
        self.source_path = source_path

    def remove_existing_rpm_package(self):
        """Removes any version that satisfies the package name of the given
        source path.
        """
        package_name = self.get_rpm_package_name()
        if self._is_package_installed(package_name):
            print('Removing existing package sources for package '
                            'with name: {0}'.format(package_name))
            sudo(['rpm', '--noscripts', '-e', package_name])

    @staticmethod
    def _is_package_installed(name):
        installed = run(['rpm', '-q', name], ignore_failures=True)
        if installed.returncode == 0:
            return True
        return False

    def is_rpm_installed(self):
        """Returns true if provided rpm is already installed.
        """
        src_query = run(['rpm', '-qp', self.source_path])
        source_name = src_query.aggr_stdout.rstrip('\n\r')

        return self._is_package_installed(source_name)

    def get_rpm_package_name(self):
        """Returns the package name according to the info provided in the source
        file.
        """
        split_index = ' : '
        package_details = {}
        package_details_query = run(['rpm', '-qpi', self.source_path])
        rows = package_details_query.aggr_stdout.split('\n')
        # split raw data according to the ' : ' index
        for row in rows:
            if split_index in row:
                first_columb_index = row.index(split_index)
                key = row[:first_columb_index].strip()
                value = row[first_columb_index + len(split_index):].strip()
                package_details[key] = value
        return package_details['Name']


def replace_in_file(this, with_this, in_here):
    """Replaces all occurences of the regex in all matches
    from a file with a specific value.
    """
    print('Replacing {0} with {1} in {2}...'.format(
        this, with_this, in_here))
    with open(in_here) as f:
        content = f.read()
    new_content = re.sub(this, with_this, content)
    fd, temp_file = tempfile.mkstemp()
    os.close(fd)
    with open(temp_file, 'w') as f:
        f.write(new_content)
    move(temp_file, in_here)


def get_selinux_state():
    return subprocess.check_output('getenforce').rstrip('\n\r')


def set_selinux_permissive():
    """This sets SELinux to permissive mode both for the current session
    and systemwide.
    """
    print('Checking whether SELinux in enforced...')
    if 'Enforcing' == get_selinux_state():
        print('SELinux is enforcing, setting permissive state...')
        sudo(['setenforce', 'permissive'])
        replace_in_file(
            'SELINUX=enforcing',
            'SELINUX=permissive',
            '/etc/selinux/config')
    else:
        print('SELinux is not enforced.')


def create_service_user(user, home):
    """Creates a user.

    It will not create the home dir for it and assume that it already exists.
    This user will only be created if it didn't already exist.
    """
    print('Checking whether user {0} exists...'.format(user))
    try:
        pwd.getpwnam(user)
        print('User {0} already exists...'.format(user))
    except KeyError:
        print('Creating user {0}, home: {1}...'.format(user, home))
        sudo(['useradd', '--shell', '/sbin/nologin', '--home-dir', home,
              '--no-create-home', '--system', user])

def chmod(mode, path):
    print('chmoding {0}: {1}'.format(path, mode))
    sudo(['chmod', mode, path])


def chown(user, group, path):
    print('chowning {0} by {1}:{2}...'.format(path, user, group))
    sudo(['chown', '-R', '{0}:{1}'.format(user, group), path])


def ln(source, target, params=None):
    print('Softlinking {0} to {1} with params {2}'.format(
        source, target, params))
    command = ['ln']
    if params:
        command.append(params)
    command.append(source)
    command.append(target)
    if '*' in source or '*' in target:
        sudo(command, globx=True)
    else:
        sudo(command)

def untar(source, destination='/tmp', strip=1, skip_old_files=False):
    # TODO: use tarfile instead
    print('Extracting {0} to {1}...'.format(source, destination))
    tar_command = ['tar', '-xzvf', source, '-C', destination,
                   '--strip={0}'.format(strip)]
    if skip_old_files:
        tar_command.append('--skip-old-files')
    sudo(tar_command)


def validate_md5_checksum(resource_path, md5_checksum_file_path):
    print('Validating md5 checksum for {0}'.format(resource_path))
    with open(md5_checksum_file_path) as checksum_file:
        original_md5 = checksum_file.read().rstrip('\n\r').split()[0]

    with open(resource_path) as file_to_check:
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()

    if original_md5 == md5_returned:
        return True
    else:
        print(
            'md5 checksum validation failed! Original checksum: {0} '
            'Calculated checksum: {1}.'.format(original_md5, md5_returned))
        return False


def write_to_json_file(content, file_path):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    mkdir(os.path.dirname(os.path.abspath(file_path)))
    with open(tmp_file.name, 'w') as f:
        f.write(json.dumps(content))
    move(tmp_file.name, file_path)


def repetitive(condition_func,
               timeout=15,
               interval=3,
               timeout_msg='timed out',
               *args,
               **kwargs):

    deadline = time.time() + timeout
    while True:
        if time.time() > deadline:
            print (timeout_msg)
        if condition_func(*args, **kwargs):
            return
        time.sleep(interval)


def http_request(url, data=None, method='PUT',
                 headers=None, timeout=None, should_fail=False):
    headers = headers or {}
    request = urllib2.Request(url, data=data, headers=headers)
    request.get_method = lambda: method
    try:
        if timeout:
            return urllib2.urlopen(request, timeout=timeout)
        return urllib2.urlopen(request)
    except urllib2.URLError as e:
        if not should_fail:
            print('Failed to {0} {1} (reason: {2})'.format(
                method, url, e.reason))


def check_http_response(url, predicate=None, **request_kwargs):
    req = urllib2.Request(url, **request_kwargs)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        # HTTPError can also be used as a non-200 response. Pass this
        # through to the predicate function, so it can decide if a
        # non-200 response is fine or not.
        response = e

    if predicate is not None and not predicate(response):
        raise ValueError(response)
    return response


