<template>
  <div id="app">
    <transition name="fade" v-if="showAnimation">
      <div id="animation" @click="skipAnimation">
        <img :src="require('@/开场动画.gif')" alt="Loading animation" class="full-screen"/>
      </div>
    </transition>
      <div id ="loginview">
      <h1 class="title">台风路径预测</h1>
      <el-form id="loginput" 
        :model="ruleForm"
        status-icon
        :rules="Loginrules"
        ref="ruleForm">        
        <el-form-item prop="account_id">
          <b><label id="LoginAccount" for="account" >账号：</label></b><br>
          <el-input width=250px v-model="ruleForm.account_id" ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <b><label id="LoginPassword" for="password">密码：</label></b><br>
          <el-input type="password" v-model="ruleForm.password" 
           @focus="showLeftImageA=false" @blur="showLeftImageA=true"></el-input>        
        </el-form-item>
        <img :src="showLeftImageA ? require('@/睁眼.png') : require('@/闭眼.png')" alt="Your Image" id="left-image"/>
      </el-form>
      <!-- 切换按钮 -->
      <div class="login-container" id="loginbutton"> 
        <button class="button Login" @click="submitForm('ruleForm')">登录</button>
        <router-link to="/regist"><button class="button toRegist">注册</button><br /></router-link>
      </div>
    </div>
  </div>
</template>

<script>


export default {
  
  data() {
    return {
     
      showLeftImageA: true,  // 初始状态下显示图片A
      showAnimation: true,
      ruleForm: {
        account_id: "",
        password: "",
      },
      Loginrules: {
        account_id: [
          { required: true, message: "用户名不能为空！", trigger: "blur" },
        ],
        password: [
          { required: true, message: "密码不能为空！", trigger: "blur" },
        ],
      },
    };
  },
  methods:{
    
    skipAnimation() {
      this.showAnimation = false;
    },
    submitForm(formName) {
  // 验证表单中的账号密码是否有效，因为在上面rules中定义为了必填 required: true
  this.$refs[formName].validate((valid) => {
    // 点击登录后，让登录按钮开始转圈圈（展示加载动画）
    this.loading = true;
    // 如果经过校验，账号密码都不为空，则发送请求到后端登录接口
    if (valid) {
      let _this = this;
      // 使用 axios 将登录信息发送到后端
      this.axios({
        url: "http://192.168.222.213:8080/login",               // 请求地址
        method: "post",                       // 请求方法
        headers: {                            // 请求头
          "Content-Type": "application/json",
        },
        data:  {
          account_id: this.ruleForm.account_id,
          password: this.ruleForm.password
        },
      }).then((res) => { // 当收到后端的响应时执行该括号内的代码，res 为响应信息，也就是后端返回的信息
            if (res.data.success === true) {  // 当响应的编码为 0 时，说明登录成功
              // 将用户信息存储到sessionStorage中
              if (res.data && res.data.cookie) {
              this.$cookies.set("account_id",res.data.cookie.account_id, "1d")
              // 现在，cookie已经被移动到响应体中。这意味着你需要从 res.data.cookie 中获取account_id和isAdmin，而不是从 res.data.user_info 中获取
            } else {
              // handle error, res.data.cookie is undefined
            }

              // 跳转页面到首页
              this.$router.push('/home').catch((error)=>{alert('请先登录')  ;console.log(error) });
              // 显示后端响应的成功信息
              this.$message({
                message: res.data.msg,
                type: "success",
              });
            } else {   // 当响应的编码不为 0 时，说明登录失败
              // 显示后端响应的失败信息
              this.$message({
                message: res.data.msg,
                type: "warning",
              });
            }
            // 不管响应成功还是失败，收到后端响应的消息后就不再让登录按钮显示加载动画了
            _this.loading = false;
            console.log(res);
          });
        } else {  // 如果账号或密码有一个没填，就直接提示必填，不向后端请求
          console.log("error submit!!");
          this.loading = false;
          return false;
        }
      });
    },
  }
}

</script>

<style>




fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
/* 文字的位置 */
label {
  display: inline-block;
  margin-left: 80px; /* 调整左侧间距为 20px */
  font-family: 'Comic Sans MS', cursive, sans-serif; /* 更改字体样式 */
  color: #FFFFFF; /* 更改字体颜色为白色 */
}

/* 输入框的宽度位置 */
.el-input{
  width: 250px !important;
  margin-left: 80px;
  border-radius: 10px; /* 添加圆角 */
  border: 2px solid #FFFFFF; /* 添加白色边框 */
  box-shadow: 0px 0px 10px #FFFFFF; /* 添加白色阴影 */
}

/* 按钮位置 */
/* .login-container{
  text-align: center; /* 水平居中对齐文本  
} */
/* 标题位置 */
.title{
  text-align: center; /* 水平居中对齐文本 */ 
   font-family: 'Comic Sans MS', cursive, sans-serif; /* 更改字体样式 */
  color: #FFFFFF; /* 更改字体颜色为白色 */
}



#loginview{
  width: 400px; /* 宽度为父元素的 20% */
  margin: 20% 35% 0% 40%; /* 外边距为 20% 顶部、35% 左 40%右、0% 底部 */
  background-color: rgb(71, 128, 193); /* 背景颜色为 RGB 值 39, 96, 161 */
  opacity: 0.7; /* 不透明度为 0.7，即 70% 的透明度 */
  outline-style: ridge; /* 使用 ridge 边框样式 */
  backdrop-filter: blur(10px);
  border-radius: 10px; /* 添加圆角矩形边框 */
  border: 0px solid #ccc;
}

/* 样式规则 for your image */
#left-image {
  width: 100px;  /* Adjust as needed */
  height: 100px;  /* Adjust as needed */
}

/* 样式规则 for the animation */
.full-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 样式规则 for your image */
img {
  width: 100px;  /* Adjust as needed */
  height: 100px;  /* Adjust as needed */
}

#loginbutton {
  padding: 8px 16px; /* 内边距为8个像素顶部/底部，16个像素左右 */
  text-align: center; /* 文本居中对齐 */
  text-decoration: none; /* 去除文本装饰（如下划线） */
  font-size: 2px; /* 字体大小为2像素 */
  margin: auto; /* 外边距为4个像素顶部/底部，2个像素左右 */
  transition-duration: 0.4s; /* 过渡动画持续时间为0.4秒 */
  cursor: pointer; /* 光标样式为手型 */
}

.toRegist {
  width: 60px;
  height:40px;
  background-color: white;
  color: black;
  border: 2px solid #f44336;
}

.toRegist:hover {
  background-color: #f44336;
  color: white;
}

/* 登录 */
.Login {
  width: 60px;
  height:40px;
  background-color: white;
  color: black;
  border: 2px solid #555555;
}

.Login:hover {
  background-color: #555555;
  color: white;
}
</style>

