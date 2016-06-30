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



import  datetime
from openerp.exceptions import Warning
import logging
import xmlrpclib
from openerp.osv import fields, osv
import calendar

class saas_user_info(osv.osv):

    def _get_server_state(self,cr,uid,ids,prop, unknow_none, context=None):
        res = {}
        for user1 in self.browse(cr, uid, ids, context=context):
            host_name = user1.host_name
            url_addres = 'http://'+ user1.server.server_addres+':'+user1.server.rpc_port+'/xmlrpc/2/db'
            try:
                dbrpc = xmlrpclib.ServerProxy(url_addres)
                if dbrpc.db_exist(host_name.lower()):
                    res[user1.id] = 'Yes'
                else:
                    res[user1.id] = 'No'
            except Exception,ex:
                raise osv.except_osv(('database exist111'), ('Wrong database name %s.')% (url_addres))
        return res

    def create_use_db(self,cr,uid,ids,prop='admin',context=None):
        isSuccess = False
        for user1 in self.browse(cr, uid, ids, context=context):
            host_name = user1.host_name.lower()
            user_pass = self.pool.get('res.users').read(cr, uid, uid, ['password'])['password']
            server_pass = user1.server.server_pass
            url_addres = 'http://'+ user1.server.server_addres+':'+user1.server.rpc_port+'/xmlrpc/2/db'
            dbrpc = xmlrpclib.ServerProxy(url_addres)
            if not  dbrpc.db_exist(host_name):
                dbrpc.create_database(server_pass,host_name, False, 'en_US',prop)
            else:
                raise osv.except_osv(('database exist'), ('Wrong database name %s.')% (host_name))
        return isSuccess
    def drop_use_db(self,cr,uid,ids,prop,context=None):
        isSuccess = False
        for user1 in self.browse(cr, uid, ids, context=context):
            host_name = user1.host_name.lower()
            #user_pass = self.pool.get('res.users').read(cr, uid, uid, ['password'])['password']
            server_pass = user1.server.server_pass
            url_addres = 'http://'+ user1.server.server_addres+':'+user1.server.rpc_port+'/xmlrpc/2/db'
            dbrpc = xmlrpclib.ServerProxy(url_addres)
            if  dbrpc.db_exist(host_name):
                dbrpc.drop(server_pass,host_name)
            else:
                raise osv.except_osv(('database had droped'), ('database had droped %s.')% (host_name))
        return isSuccess
    def add_months(self,dt, months):
        month = dt.month - 1 + months
        year = dt.year + month / 12
        month = month % 12 + 1
        day = min(dt.day,calendar.monthrange(year,month)[1])
        return dt.replace(year=year, month=month, day=day)

    def _compute_exp_date(self, cr, uid, ids,prop, unknow_none, context=None):
        res = {}
        for user1 in self.browse(cr, uid, ids, context=context):
            start_date = datetime.datetime.strptime(user1.start_date,"%Y-%m-%d %H:%M:%S")
            res[user1.id] = self.add_months(start_date,int(user1.server.product_id.warranty2))
        return res

    def _get_full_url(self, cr, uid, ids,prop, unknow_none, context=None):
        res = {}
        for user1 in self.browse(cr, uid, ids, context=context):
            if user1.server.rpc_port =='80' or user1.server.rpc_port == '':
                if user1.server.is_domain is True :
                    res[user1.id] =  user1.host_name.lower() + '.'+ user1.server.server_addres
                else :
                    res[user1.id] = user1.server.server_addres + '/web?db='+ user1.host_name.lower()
            else:
                if user1.server.is_domain is True :
                    res[user1.id] =  user1.host_name.lower() + '.'+ user1.server.server_addres +':' + user1.server.rpc_port
                else :
                    res[user1.id] = user1.server.server_addres +':' + user1.server.rpc_port+'/web?db='+ user1.host_name.lower()
        return res

    def get_counter(self,cr,uid,context=None):
        myids = self.search(cr, uid, [], context=context)
        for user in self.browse(cr,uid,myids,context=context):
            res = user.counter +1;
            isTrue =   self.write(cr, uid, user.id, {'counter': res}, context=context)
        return isTrue

    _name = "saas.user.info"
    _description = "saas.user.info"
    _columns = {
        'name': fields.char('Note', required=False,track_visibility='always', help=""),
        'user': fields.many2one('res.partner', 'partner', help=""),
        'host_name': fields.char('host_name',required=True, help=""),
        'host_type': fields.char('host_type',required=False , help=""),
        'server': fields.many2one('saas.server', 'server',required=True, help=""),
        'url_addres': fields.function(_get_full_url, type='char',string='url_addres'),
        'start_date': fields.datetime('start_date',required=False, help=""),
        'end_date': fields.function(_compute_exp_date, type = 'datetime',string='end_date'),
        'product_id':fields.many2one('product.product','product_id',required = False,help=''),
        'state': fields.function(_get_server_state, type='char', string='state'),
        'counter': fields.integer('counter',required=False , help=""),
    }
    _defaults = {
        'start_date': fields.datetime.now,
    }
    _sql_constraints = [
        ('host_name_uniq', 'unique (host_name)', 'host_name must be unique !'),
    ]

class saas_server(osv.osv):
    _inherit = ['mail.thread']
    _name = "saas.server"
    _description = "saas.server"
    _columns = {
        'name': fields.char('name', required=False, help=""),
        'server_addres': fields.char('server_addres', required=True, help=""),
        'server_pass': fields.char('server_pass',required=True,help=""),
        'rpc_port': fields.char('rpc_port',required=False , help=""),
        'product_id':fields.many2one('product.product','product_id',required = True,help=''),
		'is_domain': fields.boolean('is domain', help=""),		
    }
    _defaults = {
        'rpc_port':'80',
    }
    _sql_constraints = [
    ]

class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
               'warranty2': fields.integer('warranty2', required=False,help=""),
    }
class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'saas_ids': fields.one2many('saas.user.info', 'user', 'saas ids'),
    }
    _sql_constraints = [
    ]



