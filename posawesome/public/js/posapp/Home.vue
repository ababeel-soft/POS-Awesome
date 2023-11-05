<template>
  <v-app class="container1">
    <v-main>
      <Navbar @changePage="setPage($event)"></Navbar>
      <component v-bind:is="page" class="mx-4 md-4"></component>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from './components/Navbar.vue';
import POS from './components/pos/Pos.vue';
import Payments from './components/payments/Pay.vue';
import Orders from './components/orders/Order.vue';
import Order_Ready_Call from './components/orders/Order_Ready_Call.vue';
import Order_Ready_Delivery from './components/orders/Order_Ready_Delivery.vue';
import OrderDashBoard from './components/orders/OrderDashBoard.vue';

export default {
  data: function () {
    return {
      page: 'POS',
    };
  },
  components: {
    Navbar,
    POS,
    Payments,
    Orders,
    Order_Ready_Call,
    Order_Ready_Delivery,
    OrderDashBoard
  },
  methods: {
    setPage(page) {
      if (page =="ReadyToCall"){
        page ='Order_Ready_Call'
      }
       if (page =="ReadyToDelivery"){
        page ='Order_Ready_Delivery'
      }
      this.page = page;
      
    },
    remove_frappe_nav() {
      this.$nextTick(function () {
        $('.page-head').remove();
        $('.navbar.navbar-default.navbar-fixed-top').remove();
      });
    },
  },
  mounted() {
    this.remove_frappe_nav();
  },
  updated() {},
  created: function () {
    setTimeout(() => {
      this.remove_frappe_nav();
    }, 1000);
  },
};
</script>

<style scoped>
.container1 {
  margin-top: 0px;
  font-family: "Ubuntu";
  font-size: 1rem;
.font_card{
  font-size: 1rem;
  font-family: "Ubuntu";
}
}
</style>
