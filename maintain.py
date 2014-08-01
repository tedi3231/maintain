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

class maintain_machineroom(osv.osv):
    _name = "maintain.machineroom"
    _columns = {
        "name":fields.char(string="Name",required=True,size=100),
        "remark":fields.char(string="Remark",size=500,required=True),
        "racks":fields.one2many("maintain.machineroom.rack","machineroom_id",strin="Racks"),
    }
maintain_machineroom()

class maintain_machineroom_rack(osv.osv):
    _name = "maintain.machineroom.rack"
    _columns = {
        "name":fields.char(string="Name",size=200,required=True),
        "machineroom_id":fields.many2one("maintain.machineroom",string="Machine room",required=True),
        "remark":fields.char(string="Remark",size=500,required=False),
        "ports":fields.one2many("maintain.machineroom.rack.port","machineroom_rack_id",string="Ports"),
    }
maintain_machineroom_rack()

class maintain_machineroom_rack_port(osv.osv):
    _name = "maintain.machineroom.rack.port"
    _columns = {
        "name":fields.char(string="Name",size=200,required=True),
        "machineroom_rack_id":fields.many2one("maintain.machineroom.rack",string="Machine room",required=True),
        "remark":fields.char(string="Remark",size=500,required=False),
    }
maintain_machineroom_rack_port()

class maintain_putaway(osv.osv):
    _name = "maintain.putaway"
    _description = "putaway"

    def device_manager_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("devicemanager"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'devicemanager'})

    def network_manager_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("networkmanager"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'networkmanager'})
    
    def machineroom_manager_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("machineroommanager"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'machineroommanager'})
    
    def machineroom_watchkeeper_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("machineroomwatchkeeper"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'machineroomwatchkeeper'})

    def device2_manager_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("devicemanager2"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'devicemanager2'})

    def network2_manager_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("networkmanger2"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'networkmanger2'})

    def asset_manager_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("assetmanager"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'assetmanager'})

    def facility_manager_sign(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("facilitymanager"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'facilitymanager'})

    def done(self,cr,uid,ids,context=None):
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":OPERATIONS.get("done"),"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{'state':'done'})
    """def device_manager_sign(self,cr,uid, ids,context=None):
        #print "device_manager_sign called"
        print "context is %s" % context
        state = context.get("nextstate")
        #current state
        role = context.get("role")
        operation = OPERATIONS.get(role)
        
        operation_rep = self.pool.get("maintain.putaway.log")
        id = ids and ids[0]
        operation_rep.create(cr,uid,{"putaway_id":id,"operation":operation,"responsible":uid},context=context)    
        return self.write(cr,uid,ids,{"state":state})
    """

    _columns = {
        "name":fields.char(string="ProcessId",size=100,required=True),
        "applydate":fields.datetime(string="Apply Date",required=True),
        "asset_id":fields.many2one("cmdb.asset",string="Asset",required=True),
        "machineroom":fields.many2one("maintain.machineroom",string="Machine Room"),
        "machinerack":fields.many2one("maintain.machineroom.rack",string="Machine Rack"),
        "machineport":fields.many2one("maintain.machineroom.rack.port",string="Port"),
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
    
    def act_approved(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'confirmed','fault_sign':uid},context=context)

    def act_finish_repair(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'repair','result_sign':uid},context=context)

    def act_finish_check(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'check','checksign':uid},context=context)

    def act_finish_result(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'resultcheck'},context=context)

    def act_done(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'done'},context=context)

    def get_repair_time(self,cr,uid,ids,field,arg,context=None):
        res = dict.fromkeys(ids,None)
        for id in ids:
            res[id] =200
        return res

    _columns = {
        "name":fields.char(string="Repair Order", size=100,required=True),
        "apply_time":fields.datetime(string="Apply Date",required=True),
        "asset_id":fields.many2one("cmdb.asset",string="Asset To Repaire"),
        #"asset_name":fields.related("asset_id","name",type="char",string="Asset Name"),
        #"asset_code":fields.related("asset_id","code",type="char",string="Asset Code"),
        "fault_time":fields.datetime(string="Fault Time",required=True),
        "fault_level":fields.selection([("rightnow","立即处理"),("aftershutdown","停机后处理"),("whenmaintain","保养过程中维修"),("other","其他情况")],string="Fault Level"),
        "fault_description":fields.text(string="Fault Description"),
        "fault_sign":fields.many2one("hr.employee",string="故障申请人"),

        "fault_reason":fields.selection([("operationerror","操作失误"),("qualityerror","采购配置质量问题"),("maintainovertime","超期保养"),("electricerror","电气故障")],string="Fault Reason"),
        "method_result":fields.text(string="处理方法及结果"),
        "need_products":fields.one2many("maintain.repairorder.line","repairorder_id",string="涉及的备件"),
        "result_sign":fields.many2one("hr.employee",string="处理方案签字"),

        "repair_start":fields.datetime(string ="Repair start",),
        "repair_end":fields.datetime(string="Repair end"),
        "repair_time":fields.function(get_repair_time,string="维修时间"),
        "checks":fields.one2many("maintain.repairorder.check","maintain_repairorder_id",string="验收数据"),
        "checkresult":fields.text(string="验收结果"),
        "checksign":fields.many2one("hr.employee",string="验收人"),
        
        "fault_analyze":fields.text(string="故障原因分析及结果评定"),

        "prevents":fields.one2many("maintain.repairorder.prevent","repairorder_id",string="再发防止改善措施"),
        "remark":fields.text(string="Remark"),
        "state":fields.selection([
            ('draft', '等待审批'),
            ('cancel', '取消申请'),
            ('confirmed', '审批通过'),
            ('repair','开始维修'),
            ('check', '验收通过'),
            ('resultcheck', '结果评定'),
            ('done', '维修完成')
            ],string="State"),
    }

    _defaults = {
        "state": lambda *a : "draft",
        "fault_level":lambda *a:"rightnow",
        "apply_time":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
maintain_repairorder()

class maintain_repairorder_prevent(osv.osv):
    _name = "maintain.repairorder.prevent"
    _columns = {
        "name":fields.char(string="Position"),
        "repairorder_id":fields.many2one("maintain.repairorder",string="修理单"),
        "asset_id":fields.many2one("cmdb.asset",string="设备"),
        "method":fields.char(string="预防措施", size=500 ),
        "plan_time":fields.datetime(string="计划时间"),
        "finish_time":fields.datetime(string="完成时间"),
        "duty_officer":fields.many2one("hr.employee",string="责任人"),
    }
maintain_repairorder_prevent()

class maintain_repairorder_check(osv.osv):
    _name="maintain.repairorder.check"
    _columns = {
        "name":fields.char(string="验收项",size=100,required=True),
        "maintain_repairorder_id":fields.many2one("maintain.repairorder",string="维修单"),
        "result":fields.selection([("ok","正常"),("notok","不正常")],string="验收结果"),
    }
maintain_repairorder_check()

class maintain_repairorder_line(osv.osv):
    _name = "maintain.repairorder.line"

    _columns = {
        "name":fields.char(string="Description",size=100,required=True),
        "repairorder_id":fields.many2one("maintain.repairorder","Repair Order Refence",ondelete="cascade",select=True),
        "type":fields.selection([("add","Add"),("remove","Remove")],string="Type",required=True),
        "product_id":fields.many2one("product.product","Product",required=True),
        "product_qty":fields.integer(string="Product Qty"),
        "operation_time":fields.datetime(string="Operation Time"),
    }
    _defaults = {
        "operation_time":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
maintain_repairorder_line()
