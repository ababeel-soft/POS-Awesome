import frappe
import datetime
from datetime import date
from datetime import datetime
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from frappe import get_doc,get_all,defaults,get_list,throw,session,_dict


class CustomSalesOrder(SalesOrder):

    def before_update_after_submit(self):
        self.change_state()

    def validate(self):
        self.change_state()
        
    def add_row_note(self, state):
        row = self.append('sales_order_statuses', {})
        row.from_state = state
        row.to_state = self.workflow_state
        row.user =session.user
        if self.notes:
            row.note =self.notes
            self.notes=""
        self.user=session.user
        row.time = datetime.now().time()
        row.date = date.today()
      
    def change_state(self):
        old_doc = self.get_doc_before_save()
        if old_doc:
            if(old_doc.workflow_state != self.workflow_state):
                self.add_row_note(old_doc.workflow_state)
