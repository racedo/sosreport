### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from sos.plugins import Plugin, RedHatPlugin
import os

class ldap(Plugin, RedHatPlugin):
    """LDAP related information
    """

    files = ('/etc/openldap/ldap.conf',)
    packages = ('openldap', 'nss-pam-ldapd')

    def get_ldap_opts(self):
        # capture /etc/openldap/ldap.conf options in dict
        # FIXME: possibly not hardcode these options in?
        ldapopts=["URI","BASE","TLS_CACERTDIR"]
        results={}
        tmplist=[]
        for i in ldapopts:
            t=self.doRegexFindAll(r"^(%s)\s+(.*)" % i,"/etc/openldap/ldap.conf")
            for x in t:
                results[x[0]]=x[1].rstrip("\n")
        return results

    def setup(self):
        self.addCopySpecs(["/etc/ldap.conf", "/etc/openldap", "/etc/nslcd.conf"])

    def postproc(self):
        self.doFileSub("/etc/ldap.conf", r"(\s*bindpw\s*)\S+", r"\1***")
        self.doFileSub("/etc/nslcd.conf", r"(\s*bindpw\s*)\S+", r"\1***")
