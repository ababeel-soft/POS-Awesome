<template>
  
  <v-row justify="center">    
    <v-dialog
      v-model="OrderDialog"
      max-width="600px"
      height="400px"
      @click:outside="clear_order"
    >
      <v-card>
        <v-card-title>
          <span v-if="customer" class="headline primary--text">{{
            __('Order')
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
                      dense
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
                <v-menu
                  ref="delivery_time_menu"
                  v-model="delivery_time_menu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  dense
                 
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="custom_delivery_time"
                      :label="frappe._('Delivery Time')"
                      readonly
                      dense
                      hide-details
                      v-bind="attrs"
                      v-on="on"
                      color="primary"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="custom_delivery_time"
                    color="primary"
                    @input="delivery_time_menu = false"
                  >
                  </v-date-picker>
                </v-menu>
              </v-col>

            
              <v-col cols="6">
                <v-autocomplete
                  
                  dense
                  readonly
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

               <v-col cols="6">
                <v-autocomplete
                  
                  dense
                  color="primary"
                  :label="frappe._('Workstation')"
                  v-model="workstation_search"
                  :items="workstations"
                  background-color="white"
                  :no-data-text="__('Workstations not found')"
                  v-bind:readonly="complate"
                  hide-details
                  required
                >
                </v-autocomplete>
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
 <v-row >
  <v-col>
    <v-textarea
              class="pa-0"
              outlined
              dense
              background-color="white"
              clearable
              color="primary"
              auto-grow
              rows="2"
              :label="frappe._('Notes')"
              v-model="custom_notes"
              :value="custom_notes"
            ></v-textarea>
   </v-col>
     </v-row>
          </v-container>
        </v-card-text>
         <Order></Order>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">{{
            __('Close')
          }}</v-btn>
            <v-btn color="primary"  v-if="start" dark @click="submit_dialog('Processing')">{{
            __('Start')
          }}</v-btn>
           <v-btn color="primary"  v-if="restart" dark @click="submit_dialog('Processing')">{{
            __('Restart')
          }}</v-btn>
           <v-btn color="success"  v-if="complate" dark @click="submit_dialog('Completed')">{{
            __('Complate')
          }}</v-btn>
           <v-btn color="primary"  v-if="ready" dark @click="submit_dialog('Ready To Delivery')">{{
            __('Ready')
          }}</v-btn>
           <v-btn color="#3F51B5"  v-if="reject" dark @click="submit_dialog('Quality Rejected')">{{
            __('Reject')
          }}</v-btn>
           <v-btn color="primary"  v-if="delivery" dark @click="submit_dialog('Delivery')">{{
            __('Delivery')
          }}</v-btn>
           <v-btn color="primary"  v-if="delivery_service" dark @click="submit_dialog('On Delivery')">{{
            __('Delivery Service')
          }}</v-btn>
            <v-btn color="primary"  v-if="inspect" dark @click="submit_dialog('Quality Inspection')">{{
            __('Inspect')
          }}</v-btn>
           <v-btn color="primary"  v-if="photo" dark @click="submit_dialog('Photo Done')">{{
            __('Photo')
          }}</v-btn>
        </v-card-actions>

      <v-container v-if="has_notes">
      <p style="color:red"><strong>{{ __("Notes") }}</strong></p>
      <v-data-table
      :headers="notes_headers"
      :items="order_notes"
      item-key="to_state"
      class="elevation-1 mt-0"
      v-model="order_notes"
      >

      <template v-slot:item="{ item }">
      <tr >
      <td>{{item.to_state}}</td>
      <td>{{item.note}}</td>
      </tr>

      </template>

      </v-data-table>
      </v-container>

      </v-card>
    </v-dialog>
  </v-row>
  
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    OrderDialog: false,
    delivery_date_menu:[],
    customer: '',
    contact_mobile: '',
    workflow_state: '',
    workflowstatus: [],
    workstations: [],
    workstation_search:"",
    custom_notes:'',
    order_notes:[],
    has_notes:false,
    start:false,
    complate:false,
    restart:false,
    ready:false,
    reject:false,
    delivery:false,
    delivery_service:false,
    quality_inspection:false,
    inspect:false,
    photo:false,
    delivery_date : '',
    custom_delivery_time:'',
    order_name: '',
    filterdItems: [],
    notes_headers: [ 

       
        {
          text: __("State"),
          align: "start",
          sortable: true,
          value: "to_state",
        },
        {
          text: __("Note"),
          align: "start",
          sortable: true,
          value: "note",
        },
      ]
  }),
  watch: {},
  methods: {
   
    close_dialog() {
      this.OrderDialog = false;
      this.clear_order();
    },
    clear_order() {
      customer ='',
      contact_mobile = '',
      workflow_state = '',
      workflowstatus = [],
      workstations=[],
      custom_notes ='',
      order_notes=[],
      delivery_date = '',
      order_name = '',
      filterdItems = []
     
    },
    disable_buttons(vm){
    vm.start =false,
    vm.complate =false,
    vm.restart =false,
    vm.ready =false,
    vm.reject =false,
    vm.delivery =false,
    vm.delivery_service =false,
    vm.quality_inspection =false,
    vm.inspect =false
    vm.photo=false
  },
   show_buttons(vm){
    this.disable_buttons(vm);
      switch(vm.workflow_state) {
      case "Pending":
       vm.start=true;
      break;
      case "Processing":
      vm.complate=true;
      break;
      case "Quality Inspection":
      vm.reject=true;
      vm.photo=true;
      break;
      case "Completed":
      vm.inspect=true;
      break;
      case "Quality Rejected":
      vm.restart=true;
      break;
       case "Re Processing":
      vm.complate=true;
      break;
       case "Ready To Delivery":
      vm.delivery_service=true;
      vm.delivery=true;
      break;
      case "On Delivery":
      vm.delivery=true;
      break;
      case "Photo Done":
      vm.ready=true;
      break;
      default:
      }
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
      get_workstations() {
     
      frappe.call("posawesome.posawesome.api.posapp.get_workstations")
        .then((r) => {
          if (r.message) {
            console.log(r.message);
            this.workstations = r.message;
          }
        });
    },
     show_image(item,show) {
     evntBus.$emit("open_image_dialog",item,show);
     },

    submit_dialog(new_state) {
        const vm = this;
        this.workflow_state=new_state;
        const args = {
          customer : this.customer,
          contact_mobile : this.contact_mobile,
          workflow_state : this.workflow_state,
          workstation:this.workstation_search,
          delivery_date :this.delivery_date,
          custom_notes:this.custom_notes,
          custom_delivery_time : this.custom_delivery_time,
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
              //frappe.utils.play_sound('submit');
              evntBus.$emit("show_list");
              //this.close_dialog();
              this.show_buttons(this);
              this.get_order_notes(this.order_name);
          
          },
        });
        //this.OrderDialog = false;
      
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
  },
   get_order_notes(order) {
    return frappe
      .call("posawesome.posawesome.api.sales_order.get_order_notes", {
        order:order,
      })
      .then((r) => {
        if (r.message) {

         console.log(r.message)
         this.order_notes=r.message;
         if (this.order_notes.length > 0){
          console.log(this.order_notes.length);
          this.has_notes=true;
         }else{
           this.has_notes=false;
         }
        }
      });
  },
 
  },
  created: function () {
    evntBus.$on('open_update_order', (data) => {
  
      this.OrderDialog = true;
      
      if (data) {
        this.customer= data.customer_name
        this.order_name = data.name;
        this.delivery_date = data.delivery_date;
        this.custom_delivery_time =data.custom_delivery_time;
        this.workflow_state = data.workflow_state;
        this.workstation_search = data.workstation;
        this.contact_mobile = data.contact_mobile;
        this.custom_notes="";
        this.get_order_items(data.name);
        this.get_order_notes(data.name);
      }
      this.show_buttons(this);

    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    evntBus.$on('payments_register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    this.getWorkflowState();
    this.get_workstations();
   
  
   
  },
};
</script>
