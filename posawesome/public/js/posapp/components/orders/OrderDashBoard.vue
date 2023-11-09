<template>
  <div fluid>

   <v-container>
    <v-row v-show="!dialog">
      <v-col md="2" cols="12">
        <v-btn
        block
        color="success"
        dark
        @click="get_sales_orders"
        >{{ __("Refresh") }}</v-btn
        >
        </v-col>
    </v-row>
    <v-row style=" align : center ;max-height: 250vh; max-width:105vh" class="main mx-auto lighten-5 mt-3 p-3 pb-16 overflow-y-auto">
      <v-col >
      <VueApexCharts  type="donut" :options="chartOptions" :series="series"></VueApexCharts>
      </v-col>
    </v-row>

      </v-container>
  </div>
</template>
<script>
import { evntBus } from "../../bus";

import VueApexCharts from "vue-apexcharts";
export default {
  data: function () {
    return {
      series: [],
      chartOptions: { labels: [],
                      chart: { type: 'donut',},
                       responsive: [{breakpoint: 200, options: {chart: {width: 85}, legend: {position: 'center'}}}]
      },
      };
      },

  components: {
    VueApexCharts
  },

  methods: {

    get_sales_orders(){
      const vm =this;
      frappe.call({
      method: "posawesome.posawesome.api.sales_order.get_orders_counts",
      args:{pos_profile:null},
      callback: function (r) {
      if (r.message) {
        console.log(r.message)
      evntBus.$emit('set_counts_on_dash', (r.message));
      }
      },
      });
    },
    set_by_label(item){
      console.log(item);
      this.series.push(item.count);
      var label = frappe._(item.workflow_state);
      this.chartOptions.labels.push(label);


    },

    create_opening_voucher() {
      this.dialog = true;
    },
    onInvoiceSelected(event) {
      console.log(event.item)
     // evntBus.$emit("set_customer", event.item.customer);
    },
    clear_all() {
      this.selected_mpesa_payments = [];
      this.set_payment_methods();
    },
    submit() {
      const customer = this.customer_name;
      const vm = this;
    },
  },

  computed: {  
    total_payment_methods() {
      return this.payment_methods.reduce(
        (acc, cur) => acc + flt(cur.amount),
        0
      );
    }
  },

  mounted: function () {
    this.$nextTick(function () {

    
    
      evntBus.$on('show_list',() => {
      this.get_sales_orders();
      });
    });

  
  },created: function(){

    this.get_sales_orders();
 evntBus.$on('set_counts_on_dash', (data) => {
      this.series=[];
      this.chartOptions.labels.splice(0);
      data.forEach(this.set_by_label);
    });
    
  }

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
