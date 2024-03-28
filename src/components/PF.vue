<!-- PathForecasting.vue -->
<template>
  <div class="main-content col">
    
    <el-select  v-model="selectedTyphoon" @change="handleSelectChange(selectedTyphoon)" filterable placeholder="请选择">
        <el-option v-for="ty_Data in typhoonData"  :key="ty_Data">{{ ty_Data.ty_name }}</el-option>
    </el-select>

    <br><br>
    <baidu-map class="bm-view" :center="center" :zoom="15" @ready="setBMapOptions">
      <!-- <bm-polyline :path="pointsToPath" :strokeColor="'red'" :strokeWeight="2"></bm-polyline>   折线 -->
      <bm-marker v-for="Point in Points" :value="Point.ty_name" :key="Point" :position="{ lng: Point.lon, lat: Point.lat }"  
              :dragging="false" @click="infoWindowOpen" :icon="{url:'../图标/地图-地标.png',size:{width: 15, height: 15}}">
      <bm-info-window  :show="show" @close="infoWindowClose" @open="infoWindowOpen(item)">
        经度： {{ Point.lat }}, <br>维度：{{ Point.lon }},<br> 一分钟平均最大风速{{ Point.usa_wind }}, <br>台风等级{{ Point.r }}
        </bm-info-window>
    </bm-marker>
  </baidu-map>
  <h1>双击左键放大，双击右键缩小</h1>
  </div>

</template>
  
  <script>
import BaiduMap from 'vue-baidu-map/components/map/Map.vue'

export default {
  

  data() {
    return {
      typhoonData :[],
      items: ['选项1', '选项2', '选项3'],
      // center: { lng: 116.404, lat: 39.915 },
      center: { lng: 176.404, lat: -24.915 },
      zoom: 3,
      show: false ,// 控制信息窗口的显示状态
      selectedTyphoon: '', // 保存选择的台风名称
      // markerPoint :{ lng: 116.404, lat: 39.915 },
      Points:[ {'lat': 111,'lon': -26,'usa_wind': 34, 'level7_radius': 300, 'level10_radius': 0, 'level12_radius': 0}]
    };
  },
  
  components: {
     BaiduMap,
  },
  computed: {
    pointsToPath() {
      return this.points.map(point => ({ lng: point.lon, lat: point.lat }));
    }
  },

  methods: {
     

    /* 下拉框 */
    handleSelectChange(ty_name) {
    this.$axios({
      url: 'http://192.168.222.213:8080//typhoon_predict',
      method: 'post',
      data:  {
           account_id :this.$cookies.get('account_id'),
           ty_name,
           
        },
    })
    .then(response => {
      console.log(response.data)
      if (response.data.success) {
        this.Points = response.data.result;
// 变换地图中心
        const firstPoint = this.Points[0];
      this.center = { lng: firstPoint.lon, lat: firstPoint.lat };

      } else {
        console.log(response.data.msg);
        if (response.status == 401 || response.status == 403) {
          this.$router.push('/home');
        }
      }
    })
    .catch(error => {
      console.error(error);
    });
    },


    infoWindowClose() {
      this.show = false
    },
    infoWindowOpen() {
      this.show = true
    },
    setBMapOptions () { // 在方法内部添加设置地图类型和滚轮缩放的代码
      const map = this.$refs.map.getMap();
      map.setMapType('BMap_EARTH_MAP');
      map.enableScrollWheelZoom(true);
      
    },
    // 读取台风名称列表
    getTyphoonData() {
    this.$axios({
      url: 'http://192.168.222.213:8080/typhoon_info/search',
      method: 'post',
      data:  {//////
           account_id :this.$cookies.get('account_id')
           
          
        },
    })
    .then(response => {
      console.log(response.data)
      if (response.data.success) {
        this.typhoonData = response.data.result;
      } else {
        console.log(response.data.msg);
        if (response.status == 401 || response.status == 403) {
          this.$router.push('/home');
        }
      }
    })
    .catch(error => {
      console.error(error);
    });
    },
  },



  mounted() {
    this.getTyphoonData();
  }
}
</script>

  
  <style scoped>
/* 可以在这里添加样式 */
.bm-view {
  width: 100%;
  height: 500px;
}
.el-select{
  size: 200px;
}
.main-content{
  text-align: right;
}

</style>
