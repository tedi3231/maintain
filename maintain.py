#-*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import tools
from openerp.tools.translate import _
from openerp.modules.registry import RegistryManager
import datetime

OPERATIONS = {
    "devicemanager":"市电预加电正常",
    "networkmanager":"",
    "machineroommanager":"",
    "machineroomwatchkeeper":"以上信息完整，准许设备进入机房上回。",
    "devicemanager2":"设备、走线、设备标设符合规范",
    "networkmanger2":"完成网络标识",
    "assetmanager":"完成财产标识",
    "facilitymanager":"完成电源线标识检查规范情况",
}

class maintain_putaway(osv.osv):
    _name = "maintain.putaway"
    _description = "putaway"

    def device_manager_sign(self,cr,uid,ids,context=None):
        #print "device_manager_sign called"
        print "context is %s" % context
        state = context.get("nextstate")
        role = context.get("role")
        operation = OPERATIONS.get(role)
        
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":operation,"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{"state":state})


    _columns = {
        "name":fields.char(string="ProcessId",size=100,required=True),
        "applydate":fields.datetime(string="Apply Date",required=True),
        "asset_id":fields.many2one("cmdb.asset",string="Asset",required=True),
        "machine":fields.char(string="Machine Room"),
        "rack":fields.char(string="Rock number"),
        "port":fields.char(string="Port"),
        "pdunumber":fields.char(string="PDU Number"),
        "state":fields.selection([
            ("cancel","Cancel"),
            ("draft","draft"),
            ("devicemanager","设备管理员签名"),
            ("networkmanager","网络管理员签名"),
            ("machineroommanager","机房管理员签名"),
            ("machineroomwatchkeeper","机房值班人签名"),
            ("devicemanager2","设备管理员签名"),
            ("networkmanger2","网络管理员签名"),
            ("assetmanager","资产管理员签名"),
            ("facilitymanager","设施管理员签名"),
            ("done","Complete"),
        ],string="Status"),
        "putaway_logs":fields.one2many("maintain.putaway.log","putaway_id",string="Operations"),
        "remark":fields.text(string="Remark"),
    }
    
    _defaults = {
        "state":"draft",
        "applydate":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
maintain_putaway()

class maintain_putaway_log(osv.osv):
    _name = "maintain.putaway.log"
    _description = "operation logs"
    _columns = {
        "putaway_id":fields.many2one("maintain.putaway",string="Putaway"),
        "name":fields.char(string="Remark"),
        "operation":fields.char("Operation"),
        "responsible":fields.many2one("hr.employee",string="Responsible",required=True),
        "operation_time":fields.datetime(string="Operation Time",required=True),
    }

    _defaults = {
        "operation_time":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
maintain_putaway_log()

class maintain_repairorder(osv.osv):
    _name = "maintain.repairorder"
    _description = "work order for employee"

    _columns = {
        "name":fields.char(string="Repair Order", size=100,required=True),
        "maintainer":fields.many2one("hr.employee",string="Maintainer"),
        "assettorepair":fields.many2one("cmdb.asset",string="Asset to repair"),
        "operations":fields.one2many("maintain.repairorder.line","repairorder_id",string="Operations"),
        "remark":fields.text(string="Remark"),
        "state":fields.selection([
            ('draft', 'Quotation'),
            ('cancel', 'Cancelled'),
            ('confirmed', 'Confirmed'),
            ('under_repair', 'Under Repair'),
            ('ready', 'Ready to Repair'),
            ('done', 'Repaired')
            ],string="State"),
    }

    _defaults = {
        "state": lambda *a : "draft",
    }
maintain_repairorder()

class maintain_repairorder_line(osv.osv):
    _name = "maintain.repairorder.line"

    _columns = {
        "name":fields.char(string="Description",size=100,required=True),
        "repairorder_id":fields.many2one("maintain.repairorder","Repair Order Refence",ondelete="cascade",select=True),
        "type":fields.selection([("add","Add"),("remove","Remove")],string="Type",required=True),
        "product_id":fields.many2one("product.product","Product",required=True),
        "operation_time":fields.datetime(string="Operation Time"),
    }
    _defaults = {
        "operation_time":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
maintain_repairorder_line()
