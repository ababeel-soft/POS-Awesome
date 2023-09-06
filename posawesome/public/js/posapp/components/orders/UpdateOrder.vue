<template>
  <v-row justify="center">
    <v-dialog
      v-model="OrderDialog"
      max-width="600px"
      @click:outside="clear_order"
    >
      <v-card>
        <v-card-title>
          <span v-if="customer" class="headline primary--text">{{
            __('Update Order')
          }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
            <v-col cols="6">
                <v-text-field
                  dense
                  readonly
                  color="#FF0E0E"
                  :label="frappe._('Customer Name')"
                  background-color="white"
                  hide-details
                  v-model="customer"
                ></v-text-field>
              </v-col>
              
               <v-col cols="6">
                <v-text-field
                  dense
                  readonly
                  color="#FF0E0E"
                  :label="frappe._('Mobile No')"
                  background-color="white"
                  hide-details
                  v-model="contact_mobile"
                ></v-text-field>
              </v-col>
              
              <v-col cols="6">
                <v-text-field
                  dense
                  readonly
                  color="#FF0E0E"
                  :label="frappe._('Sales Order') + ' *'"
                  background-color="white"
                  hide-details
                  v-model="order_name"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-menu
                  ref="delivery_date_menu"
                  v-model="delivery_date_menu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  dense
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="delivery_date"
                      :label="frappe._('Delivery Date')"
                      readonly
                      dense
                      clearable
                      hide-details
                      v-bind="attrs"
                      v-on="on"
                      color="primary"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="delivery_date"
                    color="primary"
                    no-title
                    scrollable
                    @input="delivery_date_menu = false"
                  >
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="primary"
                  :label="frappe._('Status') + ' *'"
                  v-model="workflow_state"
                  :items="workflowstatus"
                  background-color="white"
                  :no-data-text="__('Status not found')"
                  hide-details
                  required
                >
                </v-autocomplete>
              </v-col>
              
              <v-col cols="6" v-if="loyalty_program">
                <v-text-field
                  v-model="loyalty_program"
                  :label="frappe._('Loyalty Program')"
                  dense
                  readonly
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="6" v-if="loyalty_points">
                <v-text-field
                  v-model="loyalty_points"
                  :label="frappe._('Loyalty Points')"
                  dense
                  readonly
                  hide-details
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">{{
            __('Close')
          }}</v-btn>
          <v-btn color="success" dark @click="submit_dialog">{{
            __('Submit')
          }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    OrderDialog: false,
    pos_profile: '',
    customer: '',
    customer_name: '',
    tax_id: '',
    contact_mobile: '',
    email_id: '',
    referral_code: '',
    birthday: null,
    delivery_date_menu: false,
    status: '',
    workflowstatus: [],
    territory: '',
    territorys: [],
    genders: [],
    customer_type: 'Individual',
    gender: '',
    loyalty_points: null,
    loyalty_program: null,
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.OrderDialog = false;
      this.clear_order();
    },
    clear_order() {
      this.customer_name = '';
      this.tax_id = '';
      this.contact_mobile = '';
      this.email_id = '';
      this.referral_code = '';
      this.birthday = '';
      this.territory = frappe.defaults.get_user_default('Territory');
      this.customer = '';
      this.customer_type = 'Individual';
      this.gender = '';
      this.loyalty_points = null;
      this.loyalty_program = null;
    },
    getWorkflowState() {
      if (this.workflowstatus.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Workflow State', {
          fields: ['name'],
          limit: 1000,
          order_by: 'name',
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.workflowstatus.push(el.name);
            });
          }
        });
    },

    submit_dialog() {
      // validate if all required fields are filled
      if (!this.status) {
        evntBus.$emit('show_mesage', {
          text: __('Order status is required.'),
          color: 'error',
        });
        return;
      }
      if (this.customer_name) {
        const vm = this;
        const args = {
          customer: this.customer,
          customer_name: this.customer_name,
          company: this.pos_profile.company,
          tax_id: this.tax_id,
          contact_mobile: this.contact_mobile,
          email_id: this.email_id,
          referral_code: this.referral_code,
          birthday: this.birthday,
          customer_group: this.status,
          territory: this.territory,
          customer_type: this.customer_type,
          gender: this.gender,
          pos_profile_doc: this.pos_profile,
        };
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.create_customer',
          args: args,
          callback: (r) => {
            if (!r.exc && r.message.name) {
              let text = __('Customer created successfully.');
              if (vm.customer) {
                text = __('Customer updated successfully.');
              }
              evntBus.$emit('show_mesage', {
                text: text,
                color: 'success',
              });
              args.name = r.message.name;
              frappe.utils.play_sound('submit');
              evntBus.$emit('add_customer_to_list', args);
              evntBus.$emit('set_customer', r.message.name);
              evntBus.$emit('fetch_customer_details');
              this.close_dialog();
            } else {
              
              frappe.utils.play_sound('error');
              evntBus.$emit('show_mesage', {
                text: __('Customer creation failed.'),
                color: 'error',
              });
            }
          },
        });
        this.OrderDialog = false;
      }
    },
  },
  created: function () {
    evntBus.$on('open_update_order', (data) => {
      console.log(data);
      this.OrderDialog = true;
      if (data) {
        this.customer= data.customer_name
        this.order_name = data.name;
        this.delivery_date = data.delivery_date;
        this.workflow_state = data.workflow_state;
        this.contact_mobile = data.contact_mobile;
      }
    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    evntBus.$on('payments_register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    this.getWorkflowState();
   
    // set default values for customer group and territory from user defaults
    this.territory = frappe.defaults.get_user_default('Territory');
  },
};
</script>
