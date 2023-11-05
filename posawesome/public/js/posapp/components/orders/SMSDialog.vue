<template>
  <v-row justify="center">
 
    <v-dialog v-model="SMSDialog" max-width="500">
      <v-card>
       <v-container>

        <v-row>
       
        <v-col>
        <v-text-field
        readonly
        :label="frappe._('Recipient Person')"
        background-color="white"
        hide-details
        v-model="recipient_person"
        ></v-text-field>
        </v-col>

         <v-col>
        <v-text-field
        :label="frappe._('Recipient Phone Number')"
        background-color="white"
        hide-details
        v-model="recipient_phone_number"
        ></v-text-field>
        </v-col>

        </v-row>`
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
      :label="frappe._('Message')"
      v-model="message"
      :value="message"
      ></v-textarea>
      </v-col>
      </v-container>
      </v-row>

        <v-row>
        <v-col>
         <v-btn color="success" width="100px"  dark @click="send_sms()">{{
            __('Send')
          }}</v-btn>
        </v-col>
        </v-row>
         </v-container>
      </v-card>

    </v-dialog>
   
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    SMSDialog: false,
    recipient_person:'',
    recipient_phone_number:'',
    message:''
  }),

  methods: {
    close_dialog() {
      this.recipient_person='',
      this.recipient_phone_number='',
      this.message=''
      this.SMSDialog = false;
    },
    send_sms() {
      let rec_num = this.recipient_phone_number;
      if(this.message.length<1){
      evntBus.$emit("show_mesage", {
      text: frappe._("Please Fill Message"),
      color: "error",
      });
      return;
      }

      if(this.recipient_phone_number.length<1){
      evntBus.$emit("show_mesage", {
      text: frappe._("Please Fill Phone Number"),
      color: "error",
      });

      return;
      }

      if(rec_num.length!=10 && rec_num.length!=9 && rec_num.length!=12 ){
      evntBus.$emit("show_mesage", {
      text: frappe._("Number Not Valied"),
      color: "error",
      });

      return;
      }


      evntBus.$emit("show_mesage", {
      text: frappe._("Message Sent Successfully"),
      color: "success",
      });
      evntBus.$emit('change_order_state','Message Sent Done');
      this.close_dialog();
    },
  },
  created: function () {
    evntBus.$on('open_sms_dialog', (data) => {
      this.SMSDialog =true;

      this.recipient_person='',
      this.recipient_phone_number='',
      this.message=''

      let order_data = data.order_doc;
      if (order_data.recipient_phone_number){
        this.recipient_person=order_data.recipient_person;
        this.recipient_phone_number=order_data.recipient_phone_number;

      }else if(order_data.contact_mobile){
        this.recipient_person=order_data.customer;
        this.recipient_phone_number=order_data.contact_mobile;
      }
       this.message="test"+order_data.name;
     
    });
  },
};
</script>
