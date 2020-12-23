 <template>
 <div> 
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark bg-light">
      <b-button class="navbar-brand bg-dark" pill @click="$router.replace({path:'/home'}).catch(err => {})" >Image Repository</b-button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <b-button class="navbar bg-dark my-profile" pill @click="$router.replace({name: 'MyProfile'}).catch(err => {})" v-if="$store.state.isLoggedIn"  >My Profile</b-button>
          <li class="nav-item active">
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
          <b-button class="navbar bg-dark" pill @click="$router.replace({name: 'images'}).catch(err => {})" >Public Images</b-button>
          </li>
        </ul>
      </div>
      <slot/>
      <b-button class=" logout bg-dark" pill @click="logout" v-if="$store.state.isLoggedIn" >Logout</b-button>
    </nav>
  </div>
</template>
<script>
export default {
  
  name: 'Header',
  methods: {
    logout() {
      this.$store.dispatch("setToken", null)
      this.$store.dispatch("setIsLoggedIn", false)
      this.$store.dispatch("setUser", null)
      this.$router.replace({path: "/home"}).catch(() => {})
    }
  }
}
</script>

<style scoped>
.container{
  max-width: 90%;
}
.my-profile{
  margin-right: 10px;
}
.logout {
margin-left: 10px;
}
</style>