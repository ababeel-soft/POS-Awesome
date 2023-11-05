<template>
  <v-row justify="center">
    <v-dialog v-model="deliveryChargeDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline primary--text">{{
            __('Update / New Address')
          }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Address')"
                  background-color="white"
                  hide-details
                  v-model="delivery_charge_doc.delivery_charge"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Price List Rate')"
                  background-color="white"
                  hide-details
                  v-model="delivery_charge_doc.delivery_charge_rate"
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
    deliveryChargeDialog:false,
    delivery_charge_doc:{},

  }),

  methods: {
    close_dialog() {
      this.deliveryChargeDialog = false;
    },
    submit_dialog() {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.make_delivery_charge',
        args: {
          args: this.delivery_charge_doc,
        },
        callback: (r) => {
          if (!r.exc) {
            evntBus.$emit('add_the_new_delivery_charge', r.message);
            evntBus.$emit('show_mesage', {
              text: 'Address created successfully.',
              color: 'success',
            });
            vm.deliveryChargeDialog = false;
            vm.delivery_charge_doc = {};
          }
        },
      });
    },
  },
  created: function () {
    evntBus.$on('open_new_delivery_charge', (pos_profile) => {
      this.deliveryChargeDialog = true;
      this.delivery_charge_doc.pos_profile=pos_profile;
    });
  },
};
</script>
