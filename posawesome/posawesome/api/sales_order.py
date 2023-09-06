# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

import frappe, erpnext, json
from frappe import _



@frappe.whitelist()
def get_orders(company, currency, customer=None, sales_order_search=None,order_status_search=""):
    filters={}
    fields=[
                "name",
                "customer",
                "customer_name",
                "grand_total",
                "currency",
                "delivery_date",
                "workflow_state",
                "contact_mobile"
            ]
    orders_list = []
    if sales_order_search:
        filters.update({"name": sales_order_search})
    if order_status_search !="":
        filters.update({"workflow_state": order_status_search})
    if customer:
      
        filters.update({"customer": customer})
        orders_docs_list =frappe.get_all("Sales Order",filters=filters,fields=fields)
        
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

        if customer:
            filters.update({"customer": customer})
        orders = frappe.get_all(
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
