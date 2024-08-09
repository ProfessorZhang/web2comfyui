<template>
  <el-dropdown size="small" class="d2-mr">
    <span class="btn-text">{{info.name ? `${info.name}` : '未登录'}}</span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item @click.native="logOff('logout')">
        <d2-icon name="sign-out" class="d2-mr-5"/>
        注销
      </el-dropdown-item>
      <el-dropdown-item @click.native="logOff('login')">
        <d2-icon name="sign-in" class="d2-mr-5"/>
        登录
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  computed: {
    ...mapState('d2admin/user', [
      'info'
    ])
  },
  methods: {
    ...mapActions('d2admin/account', [
      'logout'
    ]),
    /**
     * @description 登出
     */
    logOff (action) {
      if (action === 'logout') {
        this.logout({
          confirm: true
        })
      } else if (action === 'login') {
        this.$router.push({ name: 'login' }) // 跳转到登录页面
      }
    // logOff () {
    //   this.logout({
    //     confirm: true
    //   })
    // }
    }
  }
}
</script>
