<template>
  <v-row justify="center">
 
    <v-dialog v-model="QTYDialog" max-width="250px">
      <v-card>
       <v-container>

        <v-row>
        <v-col>
        <v-text-field
        readonly
        :label="frappe._('Item Name')"
        background-color="white"
        hide-details
        v-model="item_name"
        ></v-text-field>
        </v-col>

        </v-row>`
        <v-row>
        <v-col>
        <v-btn
        icon
        color="secondary"
         @click.stop="add_one(item)"
        >
        <v-icon>mdi-plus-circle-outline</v-icon>
        </v-btn>
        </v-col>

          <v-col>
          <v-text-field
            width=200px
            dense
            outlined
            color="primary"
            :label="frappe._('QTY')"
            background-color="white"
            hide-details
            v-model.number="qty"
            type="number"
             @keydown.enter="add_item()"
          ></v-text-field>
        </v-col>
        
        
        </v-row>


        <v-row>
        <v-col>
        <v-btn
        icon
        color="secondary"
        @click.stop="subtract_one(item)"
        >
        <v-icon>mdi-minus-circle-outline</v-icon>
        </v-btn>
        </v-col>

        <v-col>
         <v-btn color="success" width="100px"  dark @click="add_item()">{{
            __('Insert')
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
    QTYDialog: false,
    parentItem: null,
    qty: 1,
    item_name:""
  }),

  methods: {
    close_dialog() {
      this.QTYDialog = false;
      this.qty=0;
      this.item_name=""
    },
    remove_item(item) {
      const index = this.items.findIndex(
        (el) => el.posa_row_id == item.posa_row_id
      );
      if (index >= 0) {
        this.items.splice(index, 1);
      }
      const idx = this.expanded.findIndex(
        (el) => el.posa_row_id == item.posa_row_id
      );
      if (idx >= 0) {
        this.expanded.splice(idx, 1);
      }
    },
    add_item() {
      this.parentItem.qty =this.qty;
      console.log(this.parentItem.qty)
      evntBus.$emit('add_item',this.parentItem);
      this.qty=0;
      this.close_dialog();
    },

    add_one(item) {
    this.qty++;
    },
    subtract_one(item) {
    if (this.qty > 1){
    this.qty--;
    }
    },
  },
  created: function () {
    evntBus.$on('open_qty_model', (item) => {
      this.item_name=item.item_code;
      this.qty=1;
      this.QTYDialog = true;
      this.parentItem = item || null;
      //this.$refs.qty.focus();
      
     
    });
  },
};
</script>
