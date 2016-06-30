# -*- coding: utf-8 -*-
##############################################################################
#
#    odoo-saas-model , Open Source Management Solution
#    Copyright (C) 2016 binhes (<http://www.binhes.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'saas server',
    'version': '1.1',
    'author': 'LHM',
    'summary': '',
    'description': """""",
    'website': 'https://www.binhes.com',
    'depends': ['product','mail'],
    'category': '',
    'sequence': 16,
    'demo': [],
    'data': [
        'view/server_view.xml',
        'view/report_server.xml',
        'view/menu_report.xml',
        'data/server_data.xml',
        'security/ir.model.access.csv',
        'security/saas_security.xml'
		
		
    ],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
