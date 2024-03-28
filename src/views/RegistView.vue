<template>
  <!-- 注册 -->
    <div id = 'registview'>
      <!-- <div>    <el-dialog title="注册成功" :visible.sync="successDialogVisible">
        <p>{{ res.data.msg }}  \n账号为{{ res.data.result.account_id }}</p>
        <div slot="footer">
          <el-button type="primary" @click="successDialogVisible = false">关闭</el-button>
        </div>
      </el-dialog>
      </div> -->

        <h1 class="title">台风路径预测</h1>
        <el-form id="registput"
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm">
          <el-form-item prop="user_name">
            <b><label id="RegistAccount" >用户名：</label></b><br>
            <el-input v-model="ruleForm.user_name"></el-input>
          </el-form-item>

          <el-form-item prop="password">
            <b><label id="RegistPassword" >密码：</label></b><br>
            <el-input type="password" v-model="ruleForm.password" ></el-input>        
          </el-form-item>

          <el-form-item prop="confirmpassword">
            <b><label id="RegistConfirmPassword" >确认密码：</label></b><br>
            <el-input type="password" v-model="ruleForm.confirmpassword" ></el-input>        
          </el-form-item>

        </el-form>
        <!-- 切换按钮 -->
        <div class="button-container" id="registbutton">
          <router-link to="/login"><button class="button toLogin">返回</button></router-link>
          <button class="button Regist" @click="submitForm('ruleForm')">注册</button><br />
        </div>
        <!-- <el-dialog title="注册成功" :visible.sync="successDialogVisible">
      <p>{{ res.data.msg }}  \n账号为{{ res.data.result.account_id }}</p>
      <div slot="footer">
        <el-button type="primary" @click="successDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog> -->
    </div>
</template>

<script>
export default {
  data() {
    var check = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var check2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        user_name: "",
        password: "",
        confirmpassword:"",
      },




      rules: {
        user_name: [
          { required: true, message: "用户名不能为空！", trigger: "blur" },
        ],
        password: [
          { required: true, validator: check, trigger: "blur" },
        ],
        confirmpassword:[
          { required:true,validator: check2,trigger:"blur"}
        ]
      },
      successDialogVisible: false,
    };
  },

  methods:{
    submitForm(formName) {
      const formData = new FormData();
      formData.append('\'user_name:\'', this.ruleForm.user_name);
      formData.append('\'password:\'', this.ruleForm.password);
      this.$refs[formName].validate((valid) => {
        this.loading = true;  // 提交按钮显示加载动画
        if (valid) {
          let _this = this;
          this.axios({     // axios 向后端发起请求
            url: "http://192.168.222.213:8080/register",  // 请求地址
            method: "post",             // 请求方法
            headers: {                  // 请求头
              "Content-Type": "application/json",
            },
            data: formData
            ,
          }).then((res) => { // 当收到后端的响应时执行该括号内的代码，res 为响应信息，也就是后端返回的信息
            if (res.data.success === true) {  // 当响应的编码为 0 时，说明注册成功
            this.successDialogVisible = true;
              // 显示后端响应的成功信息
              this.$message({
                message: res.data.msg +'  \n账号为'+res.data.result.account_id,
                type: "success",
              });
            }else{  // 当响应的编码不为 0 时，说明注册失败
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
        } else { // 如果账号或密码有一个没填，就直接提示必填，不向后端请求
          console.log("error submit!!");
          this.loading = false;
          return false;
        }
      });
    },
    
  }
}
</script>

<style >
body{
  background-image: url(/image/login.jpg);
}

/* 文字的位置 */
label {
  display: inline-block;
  margin-left: 80px; /* 调整左侧间距为 20px */
}


/* 输入框的宽度位置 */
.el-input{
  width: 250px !important;
  margin-left: 80px;
}


/* 标题位置 */
.title{
  text-align: center; /* 水平居中对齐文本 */ 
}

#registview {
  width: 400px; /* 宽度为父元素的 20% */
  margin: 20% 35% 0% 40%; /* 外边距为 20% 顶部、35% 左 40%右、0% 底部 */
  background-color: rgb(39, 96, 161); /* 背景颜色为 RGB 值 39, 96, 161 */
  opacity: 0.7; /* 不透明度为 0.7，即 70% 的透明度 */
  outline-style: ridge; /* 使用 ridge 边框样式 */
  backdrop-filter: blur(10px);
  border-radius: 10px; /* 添加圆角矩形边框 */
  border: 0px solid #ccc;
}

#registbutton {
  padding: 8px 16px; /* 内边距为8个像素顶部/底部，16个像素左右 */
  text-align: center; /* 文本居中对齐 */
  text-decoration: none; /* 去除文本装饰（如下划线） */
  font-size: 2px; /* 字体大小为2像素 */
  margin: auto; /* 外边距为4个像素顶部/底部，2个像素左右 */
  transition-duration: 0.4s; /* 过渡动画持续时间为0.4秒 */
  cursor: pointer; /* 光标样式为手型 */
}
/* 去登录 */
.toLogin {
  width: 60px;
  height:40px;
  background-color: white;
  color: black;
  border: 2px solid #f44336;
}

.toLogin:hover {
  background-color: #f44336;
  color: white;
}
/* 注册 */
.Regist {
  width: 60px;
  height:40px;
  background-color: white;
  color: black;
  border: 2px solid #555555;
}

.Regist:hover {
  background-color: #555555;
  color: white;
}
</style>