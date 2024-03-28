<!-- /typhoon/data 的 API，我们可以获取所有的台风数据。我们也需要实现添加、
  删除、编辑台风数据的功能。这需要后端提供相应的 API。对于添加台风数据，
  /typhoon/data/add 的 API；对于删除台风数据，
  /typhoon/data/delete 的 API；对于编辑台风数据，
  /typhoon/data/edit 的 API。 -->

  <!-- 在打开模态框的方法中添加了对模态框数据的初始化，添加了关闭模态框的方法，
    以及在每个 API 调用后添加了 catch 用于捕获和处理错误 -->
    <template>
  <div class="typhoon-container">
    <el-button class="add-button" type="primary" round size="small" @click="openAddModal">
      添加台风数据
    </el-button>
    <el-table :data="typhoonData" stripe border>
      <el-table-column prop="ty_name" label="台风名称"></el-table-column>
      <el-table-column prop="isPublic" label="是否公开"></el-table-column>
      <el-table-column prop="notes" label="备注"></el-table-column>
      <el-table-column prop="lat" label="纬度"></el-table-column>
      <el-table-column prop="lon" label="经度"></el-table-column>
      <el-table-column prop="dist2land" label="中心到地面的距离"></el-table-column>
      <el-table-column prop="storm_speed" label="速度"></el-table-column>
      <el-table-column prop="storm_dir" label="方向"></el-table-column>
      <el-table-column prop="usa_wind" label="一分钟平均最大风速"></el-table-column>
      <el-table-column prop="use_sshs" label="风的等级"></el-table-column>
      <el-table-column prop="basin" label="海洋"></el-table-column>
      <el-table-column prop="nature" label="台风类型"></el-table-column> 
      <el-table-column prop="track_type" label="轨迹类型"></el-table-column>           
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="small" type="danger" @click="deleteData(scope.row.ty_name)">删除</el-button><br>
          <el-button size="small" type="success" @click="openEditModal(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加台风数据的模态框 -->
    <el-dialog title="添加台风数据" :visible.sync="isAddModalOpen" width="50%" append-to-body>
      <!-- <TyphoonForm :model="addingData"/> -->
      <el-form :model="addingData"
        status-icon
        :rules="addrules"
        ref="addingData">
    
    <el-form-item prop="ty_name" label="台风名称" :label-width="formLabelWidth">
      <el-input v-model="addingData.ty_name" autocomplete="off"></el-input>
    </el-form-item>

    <el-form-item prop="isPublic" label="是否公开" :label-width="formLabelWidth">
      <el-switch v-model="isPublic" disabled></el-switch>
    </el-form-item>

        <el-form-item prop="notes" label="备注" :label-width="formLabelWidth">
      <el-input v-model="addingData.notes" autocomplete="off"></el-input>
    </el-form-item>

        <el-form-item prop="lat" label="纬度" :label-width="formLabelWidth"  >
      <el-input v-model="addingData.lat" autocomplete="off" 
      oninput="if(value>90)value=90;if(value<-90)value=-90;" type="number" :rules="[{ required: true, message: '该项不能为空', trigger: 'change' }]"></el-input>
    </el-form-item>

        <el-form-item prop="lon" label="经度" :label-width="formLabelWidth" >
      <el-input v-model="addingData.lon" autocomplete="off"  oninput="if(value>180)value=180;if(value<-180)value=-180;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="dist2land" label="中心到地面距离" :label-width="formLabelWidth">
      <el-input v-model="addingData.dist2land" autocomplete="off" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="storm_speed" label="速度" :label-width="formLabelWidth">
      <el-input v-model="addingData.storm_speed" autocomplete="off" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="storm_dir" label="方向(0——360)" :label-width="formLabelWidth">
      <el-input v-model="addingData.storm_dir" autocomplete="off"  oninput="if(value>360)value=360;if(value<0)value=0;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="usa_wind" label="一分钟平均最大风速(20——150)" :label-width="formLabelWidth">
      <el-input v-model="addingData.usa_wind" autocomplete="off"  oninput="if(value>150)value=150;if(value<20)value=20;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="usa_sshs" label="风的等级(-5——5)" :label-width="formLabelWidth">
      <el-input v-model="addingData.usa_sshs" autocomplete="off"  oninput="if(value>5)value=5;if(value<-5)value=-5;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="basin" label="海洋" :label-width="formLabelWidth">
      <el-select v-model="addingData.basin" placeholder="请选择发生区域">
        <el-option label="东太平洋" value=0></el-option>
        <el-option label="北印度洋" value=1></el-option>
        <el-option label="南大西洋" value=2></el-option>
        <el-option label="南印度洋" value=3></el-option>
        <el-option label="南太平洋" value=4></el-option>
        <el-option label="西太平洋" value=5></el-option>
      </el-select>
    </el-form-item>

    <el-form-item prop="nature" label="台风类型" :label-width="formLabelWidth">
      <el-select v-model="addingData.nature" placeholder="请选择台风类型">
        <el-option label="DS:深低压" value=0></el-option>
        <el-option label="ET:温带气旋" value=1></el-option>
        <el-option label="MX:强台风" value=2></el-option>
        <el-option label="NR:接近台风" value=3></el-option>
        <el-option label="SS:严重风暴" value=4></el-option>
        <el-option label="TS:热带风暴" value=5></el-option>
      </el-select>
    </el-form-item>

    <el-form-item prop="track_type" label="轨迹类型" :label-width="formLabelWidth">
      <el-select v-model="addingData.track_type" placeholder="请选择轨迹类型">
        <el-option label="PROVISIONAL:临时" value=0></el-option>
        <el-option label="PROVISIONAL-SPUR:临时支线" value=1></el-option>
        <el-option label="main:主线" value=2></el-option>
        <el-option label="spur-merge:支线合并" value=3></el-option>
        <el-option label="spur-other:支线其他" value=4></el-option>
        <el-option label="spur-split:支线分离" value=5></el-option>
      </el-select>
    </el-form-item>




      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closeAddModal">取 消</el-button>
        <el-button type="primary" @click="addData">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 编辑台风数据的模态框 -->
    <el-dialog title="编辑台风数据" :visible.sync="isEditModalOpen" width="50%" append-to-body>
      <!-- <TyphoonForm :model="editingData"/> -->
      <el-form :model="editingData"
        status-icon
        :rules="editrules"
        ref="editingData">
    
    <el-form-item prop="ty_name" label="台风名称" :label-width="formLabelWidth">
      <el-input v-model="editingData.ty_name" autocomplete="off" :disabled="true"></el-input>
    </el-form-item>

    <el-form-item prop="isPublic" label="是否公开" :label-width="formLabelWidth">
      <el-switch v-model="editingData.isPublic" disabled></el-switch>
    </el-form-item>

        <el-form-item prop="notes" label="备注" :label-width="formLabelWidth">
      <el-input v-model="editingData.notes" autocomplete="off"></el-input>
    </el-form-item>

        <el-form-item prop="lat" label="纬度" :label-width="formLabelWidth" >
      <el-input v-model="editingData.lat" autocomplete="off" oninput="if(value>90)value=90;if(value<-90)value=-90;" type="number"></el-input>
    </el-form-item>

        <el-form-item prop="lon" label="经度" :label-width="formLabelWidth">
      <el-input v-model="editingData.lon" autocomplete="off" oninput="if(value>180)value=180;if(value<-180)value=-180;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="dist2land" label="中心到地面距离" :label-width="formLabelWidth">
      <el-input v-model="editingData.dist2land" autocomplete="off" oninput="if(value>360)value=360;if(value<0)value=0;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="storm_speed" label="速度" :label-width="formLabelWidth">
      <el-input v-model="editingData.storm_speed" autocomplete="off"></el-input>
    </el-form-item>

    <el-form-item prop="storm_dir" label="方向(0——360)" :label-width="formLabelWidth">
      <el-input v-model="editingData.storm_dir" autocomplete="off" oninput="if(value>360)value=360;if(value<0)value=0;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="usa_wind" label="一分钟平均最大风速(20——150)" :label-width="formLabelWidth">
      <el-input v-model="editingData.usa_wind" autocomplete="off" oninput="if(value>150)value=150;if(value<20)value=20;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="usa_sshs" label="风的等级(-5——5)" :label-width="formLabelWidth">
      <el-input v-model="editingData.usa_sshs" autocomplete="off" oninput="if(value>5)value=5;if(value<-5)value=-5;" type="number"></el-input>
    </el-form-item>

    <el-form-item prop="basin" label="海洋" :label-width="formLabelWidth">
      <el-select v-model="editingData.basin" placeholder="请选择发生区域">
        <el-option label="东太平洋" value=0></el-option>
        <el-option label="北印度洋" value=1></el-option>
        <el-option label="南大西洋" value=2></el-option>
        <el-option label="南印度洋" value=3></el-option>
        <el-option label="南太平洋" value=4></el-option>
        <el-option label="西太平洋" value=5></el-option>
      </el-select>
    </el-form-item>

    <el-form-item prop="nature" label="台风类型" :label-width="formLabelWidth">
      <el-select v-model="editingData.nature" placeholder="请选择台风类型">
        <el-option label="DS:深低压" value=0></el-option>
        <el-option label="ET:温带气旋" value=1></el-option>
        <el-option label="MX:强台风" value=2></el-option>
        <el-option label="NR:接近台风" value=3></el-option>
        <el-option label="SS:严重风暴" value=4></el-option>
        <el-option label="TS:热带风暴" value=5></el-option>
      </el-select>
    </el-form-item>

    <el-form-item prop="track_type" label="轨迹类型" :label-width="formLabelWidth">
      <el-select v-model="editingData.track_type" placeholder="请选择轨迹类型">
        <el-option label="PROVISIONAL:临时" value=0></el-option>
        <el-option label="PROVISIONAL-SPUR:临时支线" value=1></el-option>
        <el-option label="main:主线" value=2></el-option>
        <el-option label="spur-merge:支线合并" value=3></el-option>
        <el-option label="spur-other:支线其他" value=4></el-option>
        <el-option label="spur-split:支线分离" value=5></el-option>
      </el-select>
    </el-form-item>




      </el-form>


      <div slot="footer" class="dialog-footer">
        <el-button @click="closeEditModal">取 消</el-button>
        <el-button type="primary" @click="() => editData(editingData.ty_name)">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      typhoonData: [],
      isAddModalOpen: false,
      addingData: { ty_name: '', isPublic: '',
        notes:'',lat:'',lon:'',dist2land:'', storm_speed:'',storm_dir:'',
        usa_wind:'',usa_sshs:'',basin:'',nature:'',track_type:''},

      isEditModalOpen: false,
      editingData: { ty_name: '', isPublic: '',
        notes:'',lat:'',lon:'',dist2land:'', storm_speed:'',storm_dir:'',
        usa_wind:'',usa_sshs:'',basin:'',nature:'',track_type:'' },

      addrules: {
        ty_name: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        lat: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        lon: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        dist2land: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        storm_speed: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        storm_dir: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        usa_wind: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        usa_sshs: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        basin: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        nature: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        track_type: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
      },

       editrules: {
        ty_name: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        lat: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        lon: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        dist2land: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        storm_speed: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        storm_dir: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        usa_wind: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        usa_sshs: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        basin: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        nature: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
        track_type: [
          { required: true, message: "不能为空！", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    openAddModal() {
      this.isAddModalOpen = true;
       this.addingData = { ty_name: '', isPublic: false, comments:'',lat:'',lon:'',dist2land:'', storm_speed:'',storm_dir:'',usa_wind:'',usa_sshs:'' ,
                          basin : '', nature:  '',track_type : ''};
  
    },
    closeAddModal() {
      this.isAddModalOpen = false;
    },
    openEditModal(data) {
      this.isEditModalOpen = true;
      this.editingData = { ...data };
    },
    closeEditModal() {
      this.isEditModalOpen = false;
    },
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
    deleteData(ty_name) {
      this.$axios({
      url: 'http://192.168.222.213:8080/typhoon_info/delete',
      method: 'post',
      data:  {//////
           account_id:this.$cookies.get('account_id'),
           ty_name,
        },
    })
    .then(response => {
      console.log(response.data)
      if (response.data.success) {
        this.typhoonData = response.data.result;
        this.getTyphoonData();
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
  addData() {
    this.$axios({
      url: 'http://192.168.222.213:8080/typhoon_info/add',
      method: 'post',
      data: {
        account_id:this.$cookies.get('account_id'),
        // addingData:this.addingData,
        ty_name: this.addingData.ty_name,
        isPublic: false, 
        notes:this.addingData.notes,
        lat:this.addingData.lat,
        lon:this.addingData.lon,
        dist2land:this.addingData.dist2land, 
        storm_speed:this.addingData.storm_speed,
        storm_dir:this.addingData.storm_dir,
        usa_wind:this.addingData.usa_wind,
        usa_sshs:this.addingData.usa_sshs ,
                          
        basin : this.addingData.basin, 
        nature:  this.addingData.nature,
        track_type : this.addingData.track_type,
        
        }
    })
    .then(response => {
      if (response.data.success) {
        this.isAddModalOpen = false;
        this.getTyphoonData();
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
  editData(ty_name) {
    this.$axios({
      url: 'http://192.168.222.213:8080/typhoon_info/alter',
      method: 'post',
      data: {
        account_id:this.$cookies.get('account_id'),
        ty_name,
        isPublic: false, 
        notes:this.editingData.notes,
        lat:this.editingData.lat,
        lon:this.editingData.lon,
        dist2land:this.editingData.dist2land, 
        storm_speed:this.editingData.storm_speed,
        storm_dir:this.editingData.storm_dir,
        usa_wind:this.editingData.usa_wind,
        usa_sshs:this.editingData.usa_sshs ,
                          
        basin : this.editingData.basin, 
        nature:  this.editingData.nature,
        track_type : this.editingData.track_type,
         }
    })
    .then(response => {
          if (response.data.success) {
            this.isEditModalOpen = false;
            this.getTyphoonData();
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
    onlynum(event){
      const input = event.target;
      const value = input.value.trim();
      const pattern = /^\d*$/; // 确保只输入数字的正则表达式

    if (!pattern.test(value)) {
      input.value = ''; // 清空非法输入
    }
    },
  },
  mounted() {
    this.getTyphoonData();
  }
};
</script>


<style scoped>
.el-table{
  width:100%;
}

</style>