import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc

def validate(doc, method):
    pass
    """
    price_list = ""
    item_price = ""
    value = frappe.get_doc("Selling Settings").selling_price_list
    value = frappe.get_vlaue("Item Price").selling_price_list

    frappe.set_value("Item Price", docname, "fieldname", "new_value")
    frappe.msgprint(str(value))
    """
