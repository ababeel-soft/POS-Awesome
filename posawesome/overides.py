import frappe
import datetime
from datetime import date
from datetime import datetime
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from frappe import get_doc,get_all,defaults,get_list,throw,session,_dict
import random

class CustomSalesOrder(SalesOrder):

    def before_submit(self):
        desc =""
        for item in self.items:
            item_doc = frappe.get_doc("Item",item.item_code)
            item_name =""
            if item_doc.variant_of:
                item_name=item_doc.variant_of
            else:
                item_name=item_doc.item_code
            
            if self.items.index(item) > 0 :
                desc+="+"
            desc+=item_name

        self.custom_order_description=desc

    def before_update_after_submit(self):
        #self.create_item()
        self.change_state()

    def validate(self):
        if self.custom_delivery_time:
            if len(self.custom_delivery_time)>10:
                self.custom_delivery_time=None
        
        self.change_state()
        
        
    def add_row_note(self, state,notes):
        row = self.append('sales_order_statuses', {})
        row.from_state = state
        row.to_state = self.workflow_state
        row.user =session.user
        if notes:
            row.note =notes
        self.user=session.user
        row.time = datetime.now().time()
        row.date = date.today()
      
    def change_state(self):
        old_doc = self.get_doc_before_save()
        if old_doc:
            if(old_doc.workflow_state != self.workflow_state):
                if self.custom_notes:
                    self.add_row_note(old_doc.workflow_state,self.custom_notes)
                    self.custom_notes=""
        else:
            if self.posa_notes:
                self.add_row_note("Draft",self.posa_notes)
            

    def create_item(self):
        if self.workflow_state=="Delivery" and self.bundle_details:
            #item
            r=random.randint(1,1000)
            old_bundle = frappe.get_doc("Item",self.bundle_details)

            image_name = frappe.db.get_value('File',{"attached_to_name":self.name,"attached_to_field":"custom_attach__order_image"}, ['name'])
            image_doc = frappe.get_doc("File",image_name)


            new_item = frappe.new_doc("Item")
            new_item.item_code=old_bundle.item_code+str(r)
            new_item.item_group=old_bundle.item_group
            new_item.is_stock_item=0
            new_item.stock_uom=old_bundle.stock_uom
            new_item.image = image_doc.file_url
            new_item.save()

            #image file
            new_image = frappe.new_doc("File")
            new_image.file_name =image_doc.file_name
            new_image.file_type =image_doc.file_type
            new_image.file_size =image_doc.file_size
            new_image.file_url =image_doc.file_url
            new_image.attached_to_docType ="Item"
            new_image.attached_to_name =new_item.name
            new_image.attached_to_field ="image"
            new_image.is_private=1
            new_image.save()

            new_item.image = image_doc.file_url
            new_item.save()

            new_bundle = frappe.new_doc("Product Bundle")
            new_bundle.new_item_code=new_item.item_code
            for prod_item in self.items:
                new_bundle_item = new_bundle.append('items', {})
                new_bundle_item.item_code=prod_item.item_code
                new_bundle_item.qty=prod_item.qty
                new_bundle_item.rate=prod_item.rate
                new_bundle_item.uom=prod_item.uom
               

            new_bundle.save()


            #print(old_bundle.name[old_bundle.name.index("-"):])
            

            #new_doc = frappe.new_doc("Item")
            #new_doc
