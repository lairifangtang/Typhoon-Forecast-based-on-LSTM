<template>
    <el-container class="row">
      <el-aside class="left-nav col">
       <video autoplay muted loop id="myVideo">
      <source src="@/背景视频.mp4" type="video/mp4">
      <!-- 浏览器不支持 Video 标签。 -->
      </video>
           <!-- 按钮声明 -->
       <button :class="{highlighted: isHighlighted1}" @click="setCurrentPage('home'); toggleHighlight1()">
        <img src="@/图标/日志.png" alt="Icon 1" class="icon">首页</button>
      <button :class="{highlighted: isHighlighted2}" @click="setCurrentPage('dataManagement'); toggleHighlight2()">
        <img src="@/图标/台风数据.png" alt="Icon 1" class="icon">台风数据管理</button>
      <button :class="{highlighted: isHighlighted3}" @click="setCurrentPage('pathForecasting'); toggleHighlight3()">
        <img src="@/图标/路径预测.png" alt="Icon 1" class="icon">台风路径预测</button>
      <button :class="{highlighted: isHighlighted4}" @click="setCurrentPage('operationLog'); toggleHighlight4()">
        <img src="@/图标/日志.png" alt="Icon 1" class="icon">操作日志</button>
        <button :class="{highlighted: isHighlighted7}" @click="setCurrentPage('showTy'); toggleHighlight7()">世界台风信息</button>
      <button :class="{highlighted: isHighlighted5}" @click="setCurrentPage('about'); toggleHighlight5()">
        <img src="@/图标/关于我们.png" alt="Icon 1" class="icon">关于我们</button>
         <!-- 当用户为管理员时显示用户信息管理按钮 -->
         <button :class="{highlighted: isHighlighted6}" @click="toggleHighlight6">用户信息管理</button>

        <!-- <button v-if="isAdmin" :class="{highlighted: isHighlighted6}" @click="setCurrentPage('UserManagement'); toggleHighlight6()">用户信息管理</button> -->
        <button @click="setCurrentPage('home'); resetHighlights()">回退</button>
      
      </el-aside>
       
      <el-container class="right-nav col">
        <el-header>台风路径预测系统</el-header>
              <!-- 首页页面 -->
        <el-main class="main-content col">
          <h1 v-if="currentPage === 'home'"></h1>
          <component v-else v-bind:is="currentComponent" />
        </el-main>
     
    </el-container>
  </el-container>
</template>

<script>
import ShowTy from '../components/ShowTy.vue'
import { mapState, mapMutations } from 'vuex'
import DataManagement from '../components/DM.vue'
import PathForecasting from '../components/PF.vue'
import OperationLog from '../components/OL.vue'
import AboutUs from '../components/AboutUs.vue'
import UserManagement from '../components/UserManagement.vue'
// import axios from 'axios';



export default {
  name: 'HomePage',

  components: {
    ShowTy,
    DataManagement,
    PathForecasting,
    OperationLog,
    AboutUs,
    UserManagement
  },

  computed: {...mapState(['currentPage']),
  currentComponent() {
    switch (this.currentPage) {
      case 'showTy':
        return 'ShowTy'
      case 'dataManagement':
        return 'DataManagement'
      case 'pathForecasting':
        return 'PathForecasting'
      case 'operationLog':
        return 'OperationLog'
      case 'about':
        return 'AboutUs'
      case 'UserManagement': // 添加这一行
        return 'UserManagement' // 添加这一行
      default:
        return null
    }}
},
  data() {
    return {
      // 界面显示

      
      // ... 高亮选中部分
      isHighlighted1: false,
      isHighlighted2: false,
      isHighlighted3: false,
      isHighlighted4: false,
      isHighlighted5: false,
      isHighlighted6: false,
      isAdmin: false // 初始时用户不是管理员
    }
  },
  methods: {
    ...mapMutations(['setCurrentPage']),
    // ... 省略其他部分
    toggleHighlight1() {
      this.resetHighlights();
      this.isHighlighted1 = true;
    },
    toggleHighlight2() {
      this.resetHighlights();
      this.isHighlighted2 = true;
    },
    toggleHighlight3() {
      this.resetHighlights();
      this.isHighlighted3 = true;
    },
    toggleHighlight4() {
      this.resetHighlights();
      this.isHighlighted4 = true;
    },
    toggleHighlight5() {
      this.resetHighlights();
      this.isHighlighted4 = true;
    },
    toggleHighlight7() {
       this.resetHighlights();
       this.isHighlighted7 = true;
     },
     async toggleHighlight6() {
    let accountId = this.$cookies.get('account_id');
    console.log('account_id from cookie:', accountId);
    if (accountId) {
        this.$axios({
            url: 'http://192.168.237.213:8080/users/isAdmin',
            method: 'post',
            data: {
                account_id: accountId
            }
        })
        .then(response => {
            const { success, isAdmin, message } = response.data;
            if (success) {
                if (isAdmin) {
                    this.resetHighlights();
                    this.isHighlighted6 = true;
                    this.setCurrentPage('UserManagement');
                } else {
                    alert('非管理员用户越权访问');
                    this.setCurrentPage('home');
                }
            } else {
                alert(message);
                this.setCurrentPage('home');
            }
        })
        .catch(error => {
            console.error(error);
            this.setCurrentPage('home');
        });
    } else {
        alert('未登录');
        this.setCurrentPage('home');
    }
},

//   我们使用axios库发送了一个GET请求到/users/isAdmin接口，传递要查询的用户ID。根据后端的响应，我们根据success字段判断请求是否成功，并根据isAdmin字段判断用户是否是管理员。如果请求失败，我们会显示后端返回的错误消息。

// 请确保后端服务器实现了/users/isAdmin接口，并按照API文档的要求处理请求并返回正确的响应。根据你提供的响应体，响应应包含message、success和isAdmin字段。
    mounted() {
      let userInfo = this.$Cookies.get('user_info');
      console.log(userInfo)
      if (userInfo) {
      userInfo = JSON.parse(userInfo);
      this.isAdmin = userInfo.isAdmin;
      }
    },

    resetHighlights() {
      this.isHighlighted1 = false;
      this.isHighlighted2 = false;
      this.isHighlighted3 = false;
      this.isHighlighted4 = false;
      this.isHighlighted5 = false;
      this.isHighlighted6 = false;
      this.isHighlighted7 = false;
    }
  },
}
</script>

<style>

.body{
background-image: url(/image/login.jpg);

}

.container {
  display: flex;
  flex-direction: column;
}

.row {
  flex-direction: row;
}

.left-nav {
  display: flex;
  flex-direction: column;
  background-color: rgb(0, 136, 255); /* 可自定义颜色 */
  padding: 10px;
  color: white;
  order:-1;
  float: left;
  width: 20%;
  height: 100%;
  position: absolute;
  overflow: auto;
  border: 2px solid #fff;
  box-shadow: 0px 0px 15px #fff;
}

.right-nav {
  display: flex; /* 声明该元素为 Flex 容器，使其内部子元素能够进行弹性布局。 */
flex-direction: column; /* 设置子元素在容器中垂直排列。 */
padding: 10px;/*  设置内边距为 10px，给子元素提供一定的空隙。 */
color: white; /* 设置文本颜色为白色。 */
order: 0; /* 控制该元素在 Flex 容器中的排列顺序，将其放在第二个位置。 */
float: right; /* 将该元素向右浮动。 */
right: 0px; /* 定位在右边距离父元素右侧 0 像素的位置。 */
width: 80%; /* 设置宽度为父元素宽度的 80%。 */
height: 100%; /* 设置高度为父元素的 100%。 */
position: absolute; /* 将该元素进行绝对定位，相对于父元素进行定位。 */
overflow: auto;/*  如果子元素内容超出容器的尺寸，自动显示滚动条。 */
border: 2px solid #fff;
  box-shadow: 0px 0px 15px #fff;
}

.el-header {
  margin:5%;
  text-align: center;
  line-height: 60px;
  font-size:80px;
}
.main-content {
  flex: 1;
  padding: 10px;
  margin: 0% 15% 10% 10%; /* 外边距为 顶部、  右、 底部、左 */
}

.main-content .h1{

  text-align: center;
  size:50px;
}

.left-nav .button {
  background: transparent;
  margin-bottom: 40px; /* 按钮间距 */
  color: inherit;
  padding: 10px; /* 增加内边距 */
  width: 100%;
  height: 600px!important;
}



.left-nav .button:hover {
  /* 鼠标悬停时改变按钮颜色 */
  background-color: #b30000 !important;
  transform: scale(1.1);
}

.highlighted {
  background-color: rgb(168, 220, 255);
}

/* 小图标样式规则 */
.icon {
  width: 20px;  /* Adjust as needed */
  height: 20px;  /* Adjust as needed */
  margin-right: 10px;
}

/* 更改页面字体 */
body, button {
  font-family: 'Comic Sans MS', sans-serif; /* 你可以选择你想要的二次元风格字体 */
}

#myVideo {
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%; 
  min-height: 100%;
  z-index: -1; /* 保证其他内容在视频之上 */
}



</style>

