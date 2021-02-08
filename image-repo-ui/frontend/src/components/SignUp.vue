<template>
<div class="container">
  <Header/>
  <div class="jumbotron">
   <div >
    <b-form class="form-container" >
      <b-form-group
        label="Email:"
        label-for="email"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="email"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Username:" label-for="username">
        <b-form-input
          id="username"
          v-model="form.username"
          placeholder="Enter username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Password:" label-for="password">
        <b-form-input
          id="password"
          v-model="form.password"
          type="password"
          placeholder="Enter Password"
          required
        ></b-form-input>
      </b-form-group>

      <b-button  @click="onSubmit" variant="primary">Submit</b-button>
    </b-form>

    <div class="alert alert-success" role="alert" style="margin-top: 20px;" v-if="success">
      Your account has been created.
    </div>
    <div class="alert alert-danger" role="alert" v-if="failure" style="margin-top: 20px;">
      {{error}}
    </div>
  </div>
  </div>
</div>

</template>

<script>
import Header from './Header.vue'
const axios = require('axios');
export default {
  components: { Header },
  data(){
    return{
      form:{
        email: null,
        username: null,
        password: null,
      },
      success: false,
      failure: false,
      error: ''
    }
  },

  methods: {
    async onSubmit(){
      var body = {username: this.form.username, password: this.form.password, email: this.form.email}
      await axios.post('http://127.0.0.1:1919/signup', body, {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        }).then((result) => {
         if(result.status == 200){
           this.success = true
           this.failure = false
           this.$router.replace({path: '/home'}).catch(()=> {})
         }
        }).catch( (err) => {
           this.error = "Username already taken"
           this.success = false
           this.failure = true
           return err
        });
    }
  },
  
  name: 'SignUp',
}
</script>
<style>

.form-container{
    margin-left: 300px;
    margin-right: 300px;
    text-align: left;
}
</style>
