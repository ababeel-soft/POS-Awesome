<template>
  
  <v-row justify="center">
      
    <v-dialog
      v-model="OrderDialog"
      max-width="600px"
      
      @click:outside="clear_order"
    >
      <v-card>
    
          <v-container>
          <v-btn color="error" style="position:absolute" :style="{ top: '5px'}" dark @click="close_dialog"  width="5px" height="15px">{{
            __('X')
          }}</v-btn>
           </v-container>
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

               <v-col cols="6"  v-if="order_doc.contact_mobile">
                <v-text-field
                  dense
                  readonly
                  color="#FF0E0E"
                  :label="frappe._('Phone Number')"
                  background-color="white"
                  hide-details
                  v-model="order_doc.contact_mobile"
                ></v-text-field>
              </v-col>

              <v-col cols="6" v-if="order_doc.recipient_person">
                <v-text-field
                  dense
                  readonly
                  color="#FF0E0E"
                  :label="frappe._('Receptor')"
                  background-color="white"
                  hide-details
                  v-model="order_doc.recipient_person"
                ></v-text-field>
              </v-col>

               <v-col cols="6"  v-if="order_doc.recipient_phone_number">
                <v-text-field
                  dense
                  readonly
                  color="#FF0E0E"
                  :label="frappe._('Receptor Phone Number')"
                  background-color="white"
                  hide-details
                  v-model="order_doc.recipient_phone_number"
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
                  v-if ="has_role('Workstation')"
                  :items="workstations"
                  background-color="white"
                  :no-data-text="__('Workstations not found')"
                  v-bind:readonly="complate"
                  hide-details
                  required
                >
                </v-autocomplete>
              </v-col>
            <v-col cols="6" v-if =bundle_details>
            <v-text-field
            dense
            readonly
            color="#FF0E0E"
            :label="frappe._('Bundle Details')"
            background-color="white"
            hide-details
            v-model="bundle_details"
            ></v-text-field>
            </v-col>

            <v-col cols="6">
            <v-text-field
            dense
            readonly
            color="#FF0E0E"
            :label="frappe._('Order Description')"
            background-color="white"
            hide-details
            v-model="order_description"
            ></v-text-field>
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
<v-container>
    <v-row v-if="photo" flex >
    
    <v-col cols="6">
      <input type="checkbox" id="RoseQuality" value="Rose Quality" v-model="checkedNames">
      <label for="RoseQuality">{{__("Rose Quality")}}</label>
    </v-col>
    <v-col cols="6">
      <input type="checkbox" id="NastroHook" value="Nastro Hook" v-model="checkedNames">
      <label for="NastroHook">{{__("Nastro Hook")}}</label>
    </v-col>
     <v-col  cols="6">
      <input type="checkbox" id="CoordinatingColors" value="Coordinating Colors" v-model="checkedNames">
      <label for="CoordinatingColors">{{__("Coordinating Colors")}}</label>
    </v-col>

     <v-col  cols="6">
      <input type="checkbox" id="PuttingGypsophiliaInPlace" value="Putting Gypsophilia In Place" v-model="checkedNames">
      <label for="Putting GypsophiliaInPlace">{{__("Putting Gypsophilia In Place")}}</label>
    </v-col>

     <v-col  cols="6">
      <input type="checkbox" id="PutRosesInGift" value="Put Roses In Gift" v-model="checkedNames">
      <label for="PutRosesInGift">{{__("Put Roses In Gift")}}</label>
    </v-col>

     <v-col  cols="6">
      <input type="checkbox" id="GiftGivingInGeneral" value="Gift Giving In General" v-model="checkedNames">
      <label for="GiftGivingInGeneral">{{__("Gift Giving In General")}}</label>
    </v-col>
   

    </v-row>
 </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn color="primary"  v-if="start" dark @click="submit_dialog('Processing')">{{
            __('Start')
          }}</v-btn>
           <v-btn color="primary"  v-if="restart" dark @click="submit_dialog('Processing')">{{
            __('Restart')
          }}</v-btn>
           <v-btn color="success"  v-if="complate" dark @click="submit_dialog('Completed')">{{
            __('Complate')
          }}</v-btn>
           <v-btn color="primary"  v-if="ready" dark @click="submit_dialog('Ready')">{{
            __('Ready')
          }}</v-btn>

          <v-btn color="primary"  v-if="ready_to_shipping" dark @click="submit_dialog('Ready To Shipping')">{{
            __('Ready To Shipping')
          }}</v-btn>

          <v-btn color="primary"  v-if="ready_to_delivery" dark @click="submit_dialog('Ready To Delivery')">{{
            __('Ready To Delivery')
          }}</v-btn>  

          <v-btn color="primary"  v-if="no_response" dark @click="submit_dialog('No Response')">{{
            __('No Response')
          }}</v-btn>

          <v-btn color="primary"  v-if="send_sms" dark @click="sms_dialog()">{{
          __('Send SMS')
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
           <v-btn color="success"  v-if="photo" dark @click="submit_dialog('Picturing')">{{
            __('Approve')
          }}</v-btn>

           <v-btn color="primary"  v-if="workstation()" dark @click="update_workstation">{{
            __('Assign')
          }}</v-btn>
        </v-card-actions>
 
      <v-row >
      <v-container>
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
      </v-container>
      </v-row>

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
      <td>{{__(item.to_state)}}</td>
      <td>{{item.note}}</td>
      </tr>

      </template>
      </v-data-table>
      </v-container>

      <v-container >
      <template v-if =bundle_details>
      <div>
      <button @click="toggleSection">{{__("Show Bundle Image") }}</button>
      </div>
      </template>

      <template v-if="showSection" >
      <v-img 
      :src=" bundle_image ||  '/assets/posawesome/js/posapp/components/pos/placeholder-image.png'"
      class="white--text align-end"
      gradient="to bottom, rgba(0,0,0,.2), rgba(0,0,0,.7)"
      >
      </v-img>
      </template>

<template>
  <div>
    <input type="file" @change="handleFileUpload" accept="image/*">
    <button @click="uploadImage">Upload Image</button>
  </div>
</template>

      </v-container>




      </v-card>
    </v-dialog>
<SMSDialog></SMSDialog>
    
  </v-row>
  
</template>

<script>
import { evntBus } from '../../bus';
import SMSDialog from "../orders/SMSDialog.vue";

export default {
  data: () => ({
    series: [12,15],
    chartOptions: {
    labels: ['Apple', 'Mango'],
    chart: {
    type: 'donut',
    },
    responsive: [{
    breakpoint: 200,
    options: {
    chart: {
    width: 85
    },
    legend: {
    position: 'center'
    }
    }
    }]
    },
    OrderDialog: false,
    delivery_date_menu:[],
    delivery_time_menu:[],
    customer: '',
    contact_mobile: '',
    workflow_state: '',
    showSection:'',
    bundle_details:'',
    selectedFile:null ,
    bundle_image:'/assets/posawesome/js/posapp/components/pos/placeholder-image.png',
    workflowstatus: [],
    workstations: [],
    workstation_search:"",
    custom_notes:'',
    order_doc:'',
    order_notes:[],
    has_notes:false,
    start:false,
    complate:false,
    restart:false,
    ready:false,
    ready_to_delivery:false,
    ready_to_shipping:false,
    no_response:false,
    send_sms:false,
    reject:false,
    delivery:false,
    delivery_service:false,
    quality_inspection:false,
    inspect:false,
    photo:false,
    delivery_date : '',
    custom_delivery_time:'',
    order_name: '',
    order_description: '',
    filterdItems: [],
    checkedNames:[],
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
  components: {
   SMSDialog
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      console.log(this.selectedFile);
    },
    uploadImage() {
      if (this.selectedFile) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/method/upload_file', true);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('X-Frappe-CSRF-Token', frappe.csrf_token);
        let form_data = new FormData();
        form_data.append('file',this.selectedFile);
        xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
        if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        var fileName = response.message.name;
        console.log('File Name:', fileName);
        } else {
        console.log('Error:', xhr.statusText);
        }
        }
        };
        xhr.send(form_data);
        
      }
    }
    ,toggleSection() {
      //this.bundle_image = 
      this.showSection = !this.showSection; // Toggle the visibility of the section
    },
   
    close_dialog() {
      this.OrderDialog = false;
      this.clear_order();
    },
    clear_order() {
      customer ='',
      contact_mobile = '',
      workflow_state = '',
      bundle_details='',
      workflowstatus = [],
      workstations=[],
      custom_notes ='',
      order_notes=[],
      delivery_date = '',
      order_name = '',
      filterdItems = [],
      bundle_image=''
     
    },
    disable_buttons(vm){
    vm.start =false,
    vm.complate =false,
    vm.restart =false,
    vm.ready =false,
    vm.ready_to_delivery=false,
    vm.reject =false,
    vm.delivery =false,
    vm.delivery_service =false,
    vm.quality_inspection =false,
    vm.inspect =false,
    vm.photo=false,
    vm.ready_to_shipping=false,
    vm.no_response=false,
    vm.send_sms=false
  },
  has_role(role){
  var has = frappe.user.has_role(role);
  if (has !=true){
    return false
  }
  return has;
  },

  workstation(){
  var has = frappe.user.has_role("Workstation");

  if (has && this.workflow_state=="Pending"){
    return true
  }
  return false;
  },
   show_buttons(vm){
    this.disable_buttons(vm);
      switch(vm.workflow_state) {
      case "Pending":
        vm.start=(true && this.has_role("Start"));
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
      vm.delivery=true;
      vm.ready_to_shipping=true;
      break;
      case "On Delivery":
      vm.delivery=true;
      break;
      case "Photo Done":
      vm.ready=true;
      break;
      case "Picturing":
      vm.ready=true;
      break;
      case "Ready To Call":
      vm.ready_to_shipping=true;
      vm.ready_to_delivery=true;
      vm.no_response=true;
      break;
      case "Ready To Shipping":
      vm.delivery_service=true;
      break;
      case "No Response":
      vm.ready_to_delivery=true;
      vm.ready_to_shipping=true;
      vm.send_sms=true;
      break;
      case "Message Sent Done":
      vm.ready_to_delivery=true;
      vm.ready_to_shipping=true;
      break;      
      default:    
      }
  },
    getWorkflowState() {
      if (this.workflowstatus.length > 0) return;
        this.get_workflow_status()
    },

     get_workflow_status() {
     
      frappe.call("posawesome.posawesome.api.posapp.get_workflow_status")
        .then((r) => {
          if (r.message) {
          this.workflowstatus =r.message;                 
        }
        });
    },

  
     get_workflow_status() {
     
      frappe.call("posawesome.posawesome.api.posapp.get_workflow_status")
        .then((r) => {
          if (r.message) {
          console.log(r.message);
          this.workflowstatus =r.message;                 
        }
        });
    },
      get_workstations() {
     
      frappe.call("posawesome.posawesome.api.posapp.get_workstations")
        .then((r) => {
          if (r.message) {
            this.workstations = r.message;
          }
        });
    },
      update_workstation() {
        if (! this.workstation_search){
        evntBus.$emit("show_mesage", {
        text: __(`Please Select Workstation`),
        color: "error",
        });
        return;
        }

        const args = {
          workstation : this.workstation_search,
          custom_notes:this.custom_notes,
          order_name :this.order_name
        };
        frappe.call({
        method: "posawesome.posawesome.api.posapp.update_workstation",
        args: args,
        callback: (r) => {
        let text = __('Assign Workstation Successfully.');
        evntBus.$emit('show_mesage', {
        text: text,
        color: 'success',
        });
        evntBus.$emit("show_list");
        this.show_buttons(this);
        this.custom_notes='';
        this.get_order_notes(this.order_name);
        },
        });
    },
     show_image(item,show) {
     evntBus.$emit("open_image_dialog",item,show);
     },

    push_item(item){
    this.custom_notes+="- "+(frappe._(item));
     },
    submit_dialog(new_state) {
        const vm = this;
        if(new_state=='Ready') {
          if(this.order_doc.shipping_address){
            new_state="Ready To Shipping"
          }else if(this.order_doc.recipient_person){
            new_state="Ready To Call"
          }else{
            new_state="Ready To Delivery"
          }
        }
        this.workflow_state=new_state;
        if (new_state =="Quality Rejected"){
        this.custom_notes+="يرجى التأكد من : "+"\n";
        this.checkedNames.forEach(this.push_item);
        }
        
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
              this.custom_notes='';
              this.get_order_notes(this.order_name);
              evntBus.$emit("update_pages");
          
          },
        });
        //this.OrderDialog = false;
      
    },
    sms_dialog() {
      evntBus.$emit("open_sms_dialog",this);
    },
    get_order_items(order) {
    return frappe
      .call("posawesome.posawesome.api.sales_order.get_order_items", {
        order:order,
      })
      .then((r) => {
        if (r.message) {
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
         this.order_notes=r.message;
         if (this.order_notes.length > 0){
          this.has_notes=true;
         }else{
           this.has_notes=false;
         }
        }
      });
  },
 
  },
  created: function () {

    this.get_workstations();
    evntBus.$on('open_update_order', (data) => {
      this.OrderDialog = true;
      if (data) {
        this.customer= data.customer_name
        this.order_name = data.name;
        this.delivery_date = data.delivery_date;
        this.custom_delivery_time =data.custom_delivery_time;
        this.workflow_state = data.workflow_state;
        this.bundle_details = data.bundle_details;
        this.workstation_search = data.workstation;
        this.contact_mobile = data.contact_mobile;
        this.custom_notes="";
        this.get_order_items(data.name);
        this.get_order_notes(data.name);
        this.order_description = data.custom_order_description
        this.order_doc=data;
        this.bundle_image=data.custom_bundle_details_image;
      }
      this.show_buttons(this);
      this.get_workstations();

    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    evntBus.$on('payments_register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    evntBus.$on('change_order_state', (new_state) => {
    this.submit_dialog(new_state);
    });
    this.getWorkflowState();
   
   
  
   
  },
};
</script>
