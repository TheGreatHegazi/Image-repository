
<template>
<div class="container">
    <Header>
      <div>
        <b-button pill class="bg-dark" @click="addImgModal">Add Public Images</b-button>
      </div>
    </Header>
    <div class="jumbotron jum ">
      <div v-if="images.length == 0 && !busy">
        <h2 class="display-6">There are no public images</h2>
      </div>
      <div class="d-flex" style="width: 110px;" v-if="busy">
        <strong>Loading...</strong>
        <b-spinner class="ml-auto"></b-spinner>
      </div>
      <div v-if="!busy" class="image-container">
      <b-card v-for="(image, i) in images" :key="i" 
        :img-src="image"
        img-alt="Image"
        img-top
        class="img"
      >
      <b-button @click="showImage(image)" variant="outline-info">Full Image</b-button>
     </b-card>
    </div>
      <b-modal v-model="showModal" scrollable centered ok-only size="xl" >
        <img :src="fullimg"/>
        <b-container fluid> 
        </b-container>
      </b-modal>
      <b-modal v-model="addModal" @ok="addImg()" title="Add Image" centered size="lg"  >
        <b-form-file 
        multiple
        v-model="imgs"
        placeholder="Choose a file or drop it here..."
        drop-placeholder="Drop file here..."
      ></b-form-file>
      
      </b-modal>
    </div>


</div>


</template>

<script>
import Header from './Header.vue';
const axios = require('axios');

export default {
  data () {
    return {
      images: [],
      fullimg: '',
      showModal: false,
      addModal: false,
      imgs: [],
      busy: false
    }
  },
  name: 'PublicImages',
  components: {
      Header
  },
  async created() {
    this.busy = true
    await this.refreshImages();
    this.busy = false

  },
  methods: {
    async refreshImages(){
      await axios.get('http://127.0.0.1:80/images/public').then((result) => {
        this.images =  result.data.imgNames.map(n => 'http://127.0.0.1:80/images/'+n);
      }).catch((err) => {
        console.log(err)
      });
    },
    showImage(image) {
      this.fullimg = image;
      this.showModal = true;
    },
    addImgModal(){
      this.addModal = true
    }, 
    async addImg() {
      this.busy = true
      var formdata = new FormData();
      this.imgs.map(i => formdata.append('images', i))
      await axios.post('http://127.0.0.1:80/images/public/bulk',
        formdata, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      ).then(function () {
        console.log('SUCCESS!!');
      })
      .catch(function () {
        console.log('FAILURE!!');
      });
      await this.refreshImages();
      this.busy = false
    }
  }
}
</script>

<style >
.image-container{
  display: flex;
  flex-flow: wrap;
  max-height: 800px;
  overflow: auto;
  padding: 5px;
}
.jum{
  padding: 10px;
  text-align: -webkit-center;
}
.img{
  margin: 17px;
  height: 187px;
  width: fit-content;

}
.card-img, .card-img-top{
  height: 110px ;
  width: 175px;
}


</style>