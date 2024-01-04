# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

import frappe, erpnext, json
from frappe import _



@frappe.whitelist()
def get_orders(company, currency, customer=None, sales_order_search=None,order_status_search="",workstation_search=""):

    filters={}
    fields=[
                "name",
                "customer",
                "recipient_person",
                "customer_name",
                "grand_total",
                "currency",
                "delivery_date",
                "workflow_state",
                "contact_mobile",
                "custom_delivery_time",
                "custom_notes",
                "workstation",
                "custom_order_description",
                "contact_mobile",
                "recipient_phone_number",
                "shipping_address",
                "bundle_details",
                "custom_bundle_details_image"

            ]

    
    
    orders_list = []
    if sales_order_search:
        filters.update({"name": sales_order_search})
    if order_status_search !="":
        filters.update({"workflow_state": order_status_search})
   
    if workstation_search !="":
        filters.update({"workstation": workstation_search})
    else:
        if "Workstation" not in frappe.get_roles():
            filters["workstation"] = ["!=",""]


    if customer:
      
        filters.update({"customer": customer})
        orders_docs_list =frappe.get_list("Sales Order",filters=filters,fields=fields)
        
        customer_name = frappe.get_cached_value("Customer", customer, "customer_name")
        
        return orders_docs_list
    else:
        filters = {
            "company": company,
            "docstatus": 1,
            "currency": currency,
        }
        if sales_order_search:
            filters.update({"name": sales_order_search})
        
        if order_status_search !="":
            filters.update({"workflow_state": order_status_search})
        
        if workstation_search !="":
            filters.update({"workstation": workstation_search})
        else:
            if "Workstation" not in frappe.get_roles():
                filters["workstation"] = ["!=",""]
        
        if customer:
            filters.update({"customer": customer})
        orders = frappe.get_list(
            "Sales Order",
            filters=filters,
            fields=fields,
            order_by="name asc",
        )
        return orders

@frappe.whitelist()
def get_available_orders(company, currency):
    orders_list = frappe.get_list(
        "Sales Order",
        filters={"docstatus": 1, "company": company, "currency": currency},
        page_length=1000,
        pluck="name",
    )
    return orders_list

@frappe.whitelist()
def update_order(workflow_state,custom_notes,order_name,workstation=None):

    doc =frappe.get_doc("Sales Order",order_name)
    doc.workflow_state=workflow_state
    if workstation:
        doc.workstation=workstation
    doc.custom_notes=custom_notes
    doc.save()


@frappe.whitelist()
def get_order_items (order):
    return frappe.get_all("Sales Order Item",fields="*",filters={"parent":order})


@frappe.whitelist()
def get_order_notes (order):
    return frappe.get_all("Sales Order State Item",fields="*",filters={"parent":order ,"note":['!=',""]})


@frappe.whitelist()
def get_orders_counts(pos_profile=None):
    
    if (pos_profile):
        values = {'pos_profile': pos_profile}
        result = frappe.db.sql("select workflow_state, count(name) as count from `tabSales Order` WHERE docstatus =1 and pos_profile =%(pos_profile)s group by (workflow_state);",values=values, as_dict=1)
    else:
        result = frappe.db.sql("select workflow_state, count(name) as count from `tabSales Order` WHERE docstatus =1 group by workflow_state ;" ,as_dict=1)
    
    return result
