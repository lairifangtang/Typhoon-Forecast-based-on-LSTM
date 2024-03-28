<template>
  <div class="main-content col">
    <div class="header">
      <h2>关于我们:</h2>
    </div>

    <!-- 这是添加的视频部分 -->
    <video autoplay muted loop id="myVideo">
      <!-- <source src="@/关于我们.mp4" type="video/mp4"> -->
      <!-- 浏览器不支持 Video 标签。 -->
      </video>
    <div class="about-us">
      <p>
        我们是研究不奇怪的交通问题の实训小组，在我们的台风路径预测系统中，您可以查看当前台风的最新路径和预测，了解台风的详细信息,同时根据天气状况制定出行计划。
        我们团队致力于为用户提供优质的服务和准确的预测结果。如果您有任何问题或建议,欢迎随时与我们♂联系♂,邮箱:21301088@bjtu.edu.com
      </p>
    </div>
  </div>
</template>

<style scoped>
  .main-content {
    background-color: rgba(0, 136, 255, 0.1); 
    color: #2f496d;
    padding: 50px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(0, 136, 255, 0.2);
  }

  .header {
    text-align: center;
    margin-bottom: 40px;
  }

  .about-us {
    text-align: justify;
    line-height: 1.6;
  }

  /* 新增的视频容器样式 */
  .video-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }

  body, button {
    font-family: 'Comic Sans MS', sans-serif;
  }

  .main-content {
  background-color: #ffffff;
}


#myVideo {
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%; 
  min-height: 100%;
}
</style>
