<template>
  <v-row justify="center">    
    <v-dialog
      v-model="ImageDialog"
      max-width="350px"
    >
      <img :src="image_src"  >

    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    ImageDialog: false,
    image_src:'/assets/posawesome/js/posapp/components/pos/placeholder-image.png',
  }),
  watch: {},

  created: function () {

     evntBus.$on('open_image_dialog', (item,show) => {
     this.image_src=item.image;
    if (show ==false){
    this.ImageDialog = show;
    }else if (show ==true){
        this.ImageDialog = show;
    }
    });   
  },
  methods:{
    activate() {
    setTimeout(() =>  this.ImageDialog = false, 10);
  },
  }
};
</script>
