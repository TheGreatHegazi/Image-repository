<template>
<div class="container">
  <Header> 
     <b-button pill class="bg-dark" @click="LoginModal" v-if="!$store.state.isLoggedIn">Login</b-button>
  </Header>
  <div class="jumbotron">
    <h1 class="display-4">Welcome To My Image Repository!</h1>
    <p class="lead">This is my Image Repository application for the shopify challenge.</p>
    <a class="btn btn-primary btn-lg" @click="$router.replace({path: '/signup'})" role="button">Sign Up</a>
  </div>

  <b-modal v-model="loginModal" @ok="Login()" title="Login" :centered="true" id="loginmodal" >
      <b-form-group id="input-group-2" label="Username:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.username"
          placeholder="Enter username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Password:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="form.password"
          type="password"
          placeholder="Enter Password"
          required
        ></b-form-input>
      </b-form-group>
      <div class="alert alert-danger" role="alert" v-if="failure" style="margin-top: 20px;">
        {{error}}
      </div>
  </b-modal>
</div>

</template>

<script>
import Header from './Header.vue'
const axios= require('axios')
export default {
  
  components: { Header },
  data(){
    return {
      loginModal: false,  
      form: {
        username: null,
        password: null,
      },
      error: null,
      failure: false,
    }
  },
  methods: {
    LoginModal(){
      this.loginModal = true
    },
    async Login() {
      var body = {username: this.form.username, password: this.form.password}
      await axios.post('http://127.0.0.1:80/login', body, {
          headers: {
            'Content-Type': 'application/json'
          }
        }).then((result) => {
         if(result.status == 200){
          this.$store.dispatch("setToken", result.data.token)
          this.$store.dispatch("setIsLoggedIn", true)
          this.$store.dispatch("setUser", this.form.username)
         }
        }).catch( (err) => {
           this.error = "Username and password do not match "
           this.success = false
           this.failure = true
           this.loginModal = true
           return err
        });
        
    }
  },
  name: 'Home',
}
</script>

