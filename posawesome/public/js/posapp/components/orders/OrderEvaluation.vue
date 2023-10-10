<template>
  
  <v-row justify="center">    
    <v-dialog
      v-model="OrderEvaluation"
      max-width="600px"
      @click:outside="clear_order"
    >
      <v-card>
        <v-card-title>
          <span v-if="customer" class="headline primary--text">{{__('Order Evaluation')}}</span>
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
            </v-row>


 <v-row>
<v-col cols="12">
 <v-data-table
              :headers="orders_headers"
              :items="sales_orders"
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
 </v-col>
 </v-row>

             <v-row justify="center">
          <v-container>
            <div>
              <v-row dense class="overflow-y-auto" style="max-height: 500px">
                <v-col
                  v-for="(item, idx) in filterdItems"
                  :key="idx"
                  xl="2"
                  lg="3"
                  md="4"
                  sm="4"
                  cols="6"
                  min-height="50"
                >
                  <v-card >
               
                    <v-img 
                      @click=" show_image(item,true)"
                      :src="
                        item.image ||
                        '/assets/posawesome/js/posapp/components/pos/placeholder-image.png'
                      "
                
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.7)"
                      height="100px"
                    >
                      <v-card-text
                        v-text="item.item_name"
                        class="text-subtitle-2 px-1 pb-2"
                      ></v-card-text>
                    </v-img>
                    <v-card-text class="text--primary pa-1">
                      <div class="text-caption primary--text accent-3">
                        {{ item.qty || 0 }} {{ item.uom || '' }}
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            
            </div>
          </v-container>
  </v-row>
          </v-container>
        </v-card-text>
         <Order></Order>
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
    OrderEvaluation: false,
    customer: '',
    contact_mobile: '',
    workflow_state: '',
    workflowstatus: [],
    delivery_date : '',
    order_name: '',
    filterdItems: [],
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.OrderEvaluation = false;
      this.clear_order();
    },
    clear_order() {
      customer ='',
      contact_mobile = '',
      workflow_state = '',
      workflowstatus = [],
      delivery_date = '',
      order_name = '',
      filterdItems = []
     
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
     show_image(item,show) {
     evntBus.$emit("open_image_dialog",item,show);
     },

    submit_dialog() {
        const vm = this;
        const args = {
          customer : this.customer,
          contact_mobile : this.contact_mobile,
          workflow_state : this.workflow_state,
          delivery_date :this.delivery_date,
          order_name : this.order_name
        };
        frappe.call({
          method: 'posawesome.posawesome.api.sales_order.update_order',
          args: args,
          callback: (r) => {

              let text = __('Order updated successfully.');
     
              evntBus.$emit('show_mesage', {
                text: text,
                color: 'success',
              });
              frappe.utils.play_sound('submit');
              evntBus.$emit("show_list");
              this.close_dialog();
          
          },
        });
        this.OrderEvaluation = false;
      
    },
    get_order_items(order) {
    return frappe
      .call("posawesome.posawesome.api.sales_order.get_order_items", {
        order:order,
      })
      .then((r) => {
        if (r.message) {

         console.log(r.message)
         this.filterdItems=r.message;
        }
      });
  }
  },
  created: function () {
    evntBus.$on('open_order_evaluation', (data) => {
      console.log(data);
      this.OrderEvaluation = true;
      
      if (data) {
        this.customer= data.customer_name
        this.order_name = data.name;
        this.delivery_date = data.delivery_date;
        this.workflow_state = data.workflow_state;
        this.contact_mobile = data.contact_mobile;
        this.get_order_items(data.name);
      }
    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    evntBus.$on('payments_register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    this.getWorkflowState();
  
   
  },
};
</script>
