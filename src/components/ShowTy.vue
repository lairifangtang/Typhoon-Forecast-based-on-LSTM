<template>
  <div>
      <div
    class="echart"
    id="basinchart"
    :style="{ float: 'left', width: '100%', height: '400px' }"
  ></div>
  <div
    class="echart"
    id="naturechart"
    :style="{ float: 'left', width: '100%', height: '400px'}"
  ></div>
  <div
    class="echart"
    id="yearchart"
    :style="{ float: 'left', width: '100%', height: '400px'}"
  ></div>
  </div>

</template>

<script>
import * as echarts from "echarts";

export default {
  data() {
    return {
      name: "台风",
      xData: ["热带风暴", "接近台风", "温带气旋", "深低压","强台风","严重风暴"], //横坐标数据
      yData: [216289, 42227, 14634, 9247,3243,1821], //纵坐标数据，与横坐标对应

      basinName:"台风",
      basinXData:["西太平洋","南印度洋","东太平洋","南太平洋","北印度洋","南大西洋"],
      basinYData:[97565,61673,46158,30300,13432,119],

      yearName:"台风",
      yearXData:["1980-1985","1985-1990","1990-1995","1995-2000","2000-2005","2005-2010","2010=2015","2015-2020"],
      yearYData:[564,588,576,555,533,509,470,543,357]
    };

  },
  mounted() {
    this.initEcharts();
  },
  methods: {
    initEcharts() {
      const option1 = {
        title: {
          text: "各性质台风数量统计",
          textStyle:{
            color:"black"
          }
        },
        tooltip: {},
        legend: {
          data: ["数量"]
        },
        xAxis: {
        data: this.xData,
        axisLabel: {
          textStyle: {
            color: "black" // 横坐标标签的颜色为红色
          }
        }
      },
      yAxis: {
        axisLabel: {
          textStyle: {
            color: "black" // 纵坐标标签的颜色为绿色
          }
        }
      },
        series: [
          {
            name: "数量",
            type: "bar", //类型为柱状图
            data: this.yData, // 使用yData作为柱状图数据
            itemStyle:{
                color:'gold'
            }
          }
        ]
      };
      const option2 = {
        title: {
          text: "各海域上的台风数量统计",
          textStyle:{
            color:"black"
          }
        },
        tooltip: {},
        legend: {
          data: ["数量"]
        },
        xAxis: {
        data: this.basinXData,
        axisLabel: {
          textStyle: {
            color: "black" // 横坐标标签的颜色为红色
          }
        }
      },
      yAxis: {
        axisLabel: {
          textStyle: {
            color: "black" // sxz纵坐标标签的颜色为绿色
          }
        }
      },
        series: [
          {
            name: "数量",
            type: "bar", //类型为柱状图
            data: this.basinYData, // 使用yData作为柱状图数据
            itemStyle:{
                color:'gold'
            }
          }
        ]
      };
      const option3 = {
        title: {
          text: "每五年台风数量统计",
          textStyle:{
            color:"black"
          }
        },
        tooltip: {},
        legend: {
          data: ["数量"]
        },
        xAxis: {
        data: this.yearXData,
        axisLabel: {
          textStyle: {
            color: "black" // 横坐标标签的颜色为红色
          }
        }
      },
      yAxis: {
        axisLabel: {
          textStyle: {
            color: "black" // 纵坐标标签的颜色为绿色
          }
        }
      },
        series: [
          {
            name: "数量",
            type: "bar", //类型为柱状图
            data: this.yearYData, // 使用yData作为柱状图数据
            itemStyle:{
                color:'gold'
            }
          }
        ]
      };
      const myChart1 = echarts.init(document.getElementById('basinchart')); // 通过ID选择器获取元素
      myChart1.setOption(option1); // 渲染页面
      // 随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        myChart1.resize();
      });
      const myChart2 = echarts.init(document.getElementById('naturechart')); // 通过ID选择器获取元素
      myChart2.setOption(option2); // 渲染页面
      // 随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        myChart2.resize();
      });
      const myChart3 = echarts.init(document.getElementById('yearchart')); // 通过ID选择器获取元素
      myChart3.setOption(option3); // 渲染页面
      // 随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        myChart3.resize();
      });
    }
  }
};
</script>

<style scoped>
.echart{

  background-color: rgb(71, 128, 193); /* 背景颜色为 RGB 值 39, 96, 161 */
  opacity: 0.7; /* 不透明度为 0.7，即 70% 的透明度 */
  outline-style: ridge; /* 使用 ridge 边框样式 */
  backdrop-filter: blur(10px);
  border-radius: 10px; /* 添加圆角矩形边框 */
  border: 0px solid #ccc;
}

</style>