<template>
  <div fluid>
    <v-row v-show="!dialog">
      <v-col md="12" cols="12" class="pb-2 pr-0">
        <v-card
          class="main mx-auto grey lighten-5 mt-3 p-3 pb-16 overflow-y-auto"
          style="max-height: 94vh; height: 94vh"
        >
          <div>
            <v-row>
            <v-col md="4" cols="12">
            <Customer></Customer>
            </v-col>
            </v-row>
            <v-row>
              <v-col md="7" cols="12">
                <p>
                  <strong>{{ __("Orders") }}</strong>
                </p>
              </v-col>
            </v-row>
            <v-row align="center" no-gutters class="mb-1">
              <v-col md="3" cols="12">
                <v-autocomplete
                  dense
                  outlined
                  hide-details
                  clearable
                  background-color="white"
                  v-model="sales_order_search"
                  :items="sales_order_list"
                  item-value="name"
                  label="Search by Name"
                  @change="get_sales_orders"
                ></v-autocomplete>
              </v-col>
               <v-col md="3" cols="8" class="ma-2"> 
                <v-select
                  dense
                  outlined
                  hide-details
                  clearable
                  background-color="white"
                  v-model="order_status_search"
                  :items="order_status_list"
                  item-value="name"
                  label="Status"
                  @change="get_sales_orders"
                ></v-select>
              </v-col>
              <v-col> </v-col>
              <v-col md="3" cols="12">
                <v-btn
                  block
                  color="warning"
                  dark
                  @click="get_sales_orders"
                  >{{ __("Search") }}</v-btn
                >
              </v-col>
            </v-row>
            <UpdateOrder></UpdateOrder>
            <v-data-table
              :headers="orders_headers"
              :items="outstanding_invoices"
              item-key="name"
              class="elevation-1 mt-0"
              v-model="selected_invoices"
              :loading="invoices_loading"
            >

          <template v-slot:item="{ item }">
          <tr @click="rowClicked(item)" >
          <td>{{item.name}}</td>
          <td>{{item.customer}}</td>
          <td>{{item.delivery_date}}</td>
          <td>{{item.grand_total}} {{ currencySymbol(pos_profile.currency) }}</td>
          <td>{{item.workflow_state}}</td>
          </tr>
          
          </template>

            </v-data-table>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { evntBus } from "../../bus";
import format from "../../format";
import Customer from "../pos/Customer.vue";
import UpdateCustomer from "../pos/UpdateCustomer.vue";
import UpdateOrder from "../orders/UpdateOrder.vue";


export default {
  mixins: [format],
  data: function () {
    return {
      dialog: false,
      pos_profile: "",
      pos_opening_shift: "",
      customer_name: "",
      customer_info: "",
      company: "",
      singleSelect: false,
      invoices_loading: false,
      unallocated_payments_loading: false,
      mpesa_payments_loading: false,
      payment_methods: [],
      outstanding_invoices: [],
      unallocated_payments: [],
      mpesa_payments: [],
      selected_invoices: [],
      selected_payments: [],
      selected_mpesa_payments: [],
      sales_order_list: [],
      order_status_list: [],
      sales_order_search: "",
      order_status_search: "",
      payment_methods_list: [],
      mpesa_searchname: "",
      mpesa_search_mobile: "",
      orders_headers: [ 

       

         {
          text: __("Order"),
          align: "start",
          sortable: true,
          value: "name",
        },
        {
          text: __("Customer"),
          align: "start",
          sortable: true,
          value: "customer_name",
        },
        {
          text: __("Delivery Date"),
          align: "start",
          sortable: true,
          value: "delivery_date",
        },
        {
          text: __("Total"),
          align: "start",
          sortable: true,
          value: "grand_total",
        },
        {
          text: __("Status"),
          align: "start",
          sortable: true,
          value: "workflow_state",
        },
      ]
    };
  },

  components: {
    Customer,
    UpdateCustomer,
    UpdateOrder,
  },

  methods: {
    check_opening_entry() {
      return frappe
        .call("posawesome.posawesome.api.posapp.check_opening_shift", {
          user: frappe.session.user,
        })
        .then((r) => {
          if (r.message) {
            this.pos_profile = r.message.pos_profile;
            this.pos_opening_shift = r.message.pos_opening_shift;
            this.company = r.message.company.name;
            evntBus.$emit("payments_register_pos_profile", r.message);
            evntBus.$emit("set_company", r.message.company);
            this.set_payment_methods();
            this.payment_methods_list = [];
            this.pos_profile.payments.forEach((element) => {
              this.payment_methods_list.push(element.mode_of_payment);
            });
            this.get_available_pos_profiles();
            this.get_sales_orders();
            this.get_draft_mpesa_payments_register();
          } else {
            this.create_opening_voucher();
          }
        });
    },
    get_available_pos_profiles() {
      if (!this.pos_profile.posa_allow_mpesa_reconcile_payments) return;
      return frappe
        .call(
          "posawesome.posawesome.api.sales_order.get_available_orders",
          {
            company: this.company,
            currency: this.pos_profile.currency,
          }
        )
        .then((r) => {
          if (r.message) {
            this.sales_order_list = r.message;
          }
        });
    },
    create_opening_voucher() {
      this.dialog = true;
    },
    fetch_customer_details() {
      const vm = this;
      if (this.customer_name) {
        frappe.call({
          method: "posawesome.posawesome.api.posapp.get_customer_info",
          args: {
            customer: vm.customer_name,
          },
          async: false,
          callback: (r) => {
            const message = r.message;
            if (!r.exc) {
              vm.customer_info = {
                ...message,
              };
              vm.set_mpesa_search_params();
              evntBus.$emit("set_customer_info_to_edit", vm.customer_info);
            }
          },
        });
      }
    },
    onInvoiceSelected(event) {
      console.log(event.item)
     // evntBus.$emit("set_customer", event.item.customer);
    },

    rowClicked(item){
      evntBus.$emit("open_update_order",item);
      //alert(item.name)
    },
    get_sales_orders() {
      this.invoices_loading = true;
      return frappe
        .call(
          "posawesome.posawesome.api.sales_order.get_orders",
          {
            customer: this.customer_name,
            company: this.company,
            currency: this.pos_profile.currency,
            sales_order_search: this.sales_order_search,
            order_status_search:this.order_status_search
          }
        )
        .then((r) => {
          if (r.message) {
            this.outstanding_invoices = r.message;
            this.invoices_loading = false;
          }
        });
    },
    get_workflow_status() {
     
      frappe.call("posawesome.posawesome.api.posapp.get_workflow_status")
        .then((r) => {
          if (r.message) {
            this.order_status_list = r.message;
          }
        });
    },

    get_unallocated_payments() {
      if (!this.pos_profile.posa_allow_reconcile_payments) return;
      this.unallocated_payments_loading = true;
      if (!this.customer_name) {
        this.unallocated_payments = [];
        this.unallocated_payments_loading = false;
        return;
      }
      return frappe
        .call(
          "posawesome.posawesome.api.payment_entry.get_unallocated_payments",
          {
            customer: this.customer_name,
            company: this.company,
            currency: this.pos_profile.currency,
          }
        )
        .then((r) => {
          if (r.message) {
            this.unallocated_payments = r.message;
            this.unallocated_payments_loading = false;
          }
        });
    },
    set_mpesa_search_params() {
      if (!this.pos_profile.posa_allow_mpesa_reconcile_payments) return;
      if (!this.customer_name) return;
      this.mpesa_search_name = this.customer_info.customer_name.split(" ")[0];
      if (this.customer_info.mobile_no) {
        this.mpesa_search_mobile =
          this.customer_info.mobile_no.substring(0, 4) +
          " ***** " +
          this.customer_info.mobile_no.substring(9);
      }
    },
    get_draft_mpesa_payments_register() {
      if (!this.pos_profile.posa_allow_mpesa_reconcile_payments) return;
      const vm = this;
      this.mpesa_payments_loading = true;
      return frappe
        .call("posawesome.posawesome.api.m_pesa.get_mpesa_draft_payments", {
          company: vm.company,
          mode_of_payment: null,
          full_name: vm.mpesa_search_name || null,
          mobile_no: vm.mpesa_search_mobile || null,
          payment_methods_list: vm.payment_methods_list,
        })
        .then((r) => {
          if (r.message) {
            vm.mpesa_payments = r.message;
          } else {
            vm.mpesa_payments = [];
          }
          vm.mpesa_payments_loading = false;
        });
    },
    set_payment_methods() {
      // get payment methods from pos profile
      if (!this.pos_profile.posa_allow_make_new_payments) return;
      this.payment_methods = [];
      this.pos_profile.payments.forEach((method) => {
        this.payment_methods.push({
          mode_of_payment: method.mode_of_payment,
          amount: 0,
          row_id: method.name,
        });
      });
    },
    clear_all(with_customer_info = true) {
      this.customer_name = "";
      if (with_customer_info) {
        this.customer_info = "";
      }
      this.mpesa_search_mobile = "";
      this.mpesa_search_name = "";
      this.mpesa_payments = [];
      this.selected_mpesa_payments = [];
      this.outstanding_invoices = [];
      this.unallocated_payments = [];
      this.selected_invoices = [];
      this.selected_payments = [];
      this.selected_mpesa_payments = [];
      this.set_payment_methods();
    },
    submit() {
      const customer = this.customer_name;
      const vm = this;
      if (!customer) {
        frappe.throw(__("Please select a customer"));
        return;
      }
      if (
        this.total_selected_payments == 0 &&
        this.total_selected_mpesa_payments == 0 &&
        this.total_payment_methods == 0
      ) {
        frappe.throw(__("Please make a payment or select an payment"));
        return;
      }
      if (
        this.total_selected_payments > 0 &&
        this.selected_invoices.length == 0
      ) {
        frappe.throw(__("Please select an invoice"));
        return;
      }

      this.payment_methods.forEach((payment) => {
        payment.amount = flt(payment.amount);
      });

      const payload = {};
      payload.customer = customer;
      payload.company = this.company;
      payload.currency = this.pos_profile.currency;
      payload.pos_opening_shift_name = this.pos_opening_shift.name;
      payload.pos_profile_name = this.pos_profile.name;
      payload.pos_profile = this.pos_profile;
      payload.payment_methods = this.payment_methods;
      payload.selected_invoices = this.selected_invoices;
      payload.selected_payments = this.selected_payments;
      payload.total_selected_invoices = flt(this.total_selected_invoices);
      payload.selected_mpesa_payments = this.selected_mpesa_payments;
      payload.total_selected_payments = flt(this.total_selected_payments);
      payload.total_payment_methods = flt(this.total_payment_methods);
      payload.total_selected_mpesa_payments = flt(
        this.total_selected_mpesa_payments
      );

      frappe.call({
        method: "posawesome.posawesome.api.payment_entry.process_pos_payment",
        args: { payload },
        freeze: true,
        freeze_message: __("Processing Payment"),
        callback: function (r) {
          if (r.message) {
            frappe.utils.play_sound("submit");
            vm.clear_all(false);
            vm.customer_name = customer;
            vm.get_sales_orders();
            vm.get_unallocated_payments();
            vm.set_mpesa_search_params();
            vm.get_draft_mpesa_payments_register();
          }
        },
      });
    },
  },

  computed: {
    total_outstanding_amount() {
      return this.outstanding_invoices.reduce(
        (acc, cur) => acc + flt(cur.outstanding_amount),
        0
      );
    },
    total_unallocated_amount() {
      return this.unallocated_payments.reduce(
        (acc, cur) => acc + flt(cur.unallocated_amount),
        0
      );
    },
    total_selected_invoices() {
      return this.selected_invoices.reduce(
        (acc, cur) => acc + flt(cur.outstanding_amount),
        0
      );
    },
    total_selected_payments() {
      return this.selected_payments.reduce(
        (acc, cur) => acc + flt(cur.unallocated_amount),
        0
      );
    },
    total_selected_mpesa_payments() {
      return this.selected_mpesa_payments.reduce(
        (acc, cur) => acc + flt(cur.amount),
        0
      );
    },
    total_payment_methods() {
      return this.payment_methods.reduce(
        (acc, cur) => acc + flt(cur.amount),
        0
      );
    },
    total_of_diff() {
      return flt(
        this.total_selected_invoices -
          this.total_selected_payments -
          this.total_selected_mpesa_payments -
          this.total_payment_methods
      );
    },
  },

  mounted: function () {
    this.$nextTick(function () {
      this.check_opening_entry();
      evntBus.$on("update_customer", (customer_name) => {
        this.clear_all(true);
        this.customer_name = customer_name;
        this.fetch_customer_details();
        this.get_sales_orders();
        this.get_unallocated_payments();
        this.get_draft_mpesa_payments_register();
      });
      evntBus.$on("fetch_customer_details", () => {
        this.fetch_customer_details();
      });
    });

    this.get_workflow_status();
  },
  beforeDestroy() {
    evntBus.$off("update_customer");
    evntBus.$off("fetch_customer_details");
  },
};
</script>

<style>
input[total_of_diff] {
  text-align: right;
}
input[payments_methods] {
  text-align: right;
}
input[total_selected_payments] {
  text-align: right;
}
input[total_selected_invoices] {
  text-align: right;
}
input[total_selected_mpesa_payments] {
  text-align: right;
}
</style>
