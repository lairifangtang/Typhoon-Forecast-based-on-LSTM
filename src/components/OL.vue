<!-- OperationLog.vue -->
<template>
  <div class="main-content col">
    <h1>操作日志</h1>
    <el-button type="danger" @click="clearLogs">清空日志</el-button>
    <el-table class="my-table" :data="operationLogs" border style="width: 100%">
      <el-table-column prop="ty_name" label="台风名称" width="180"></el-table-column>
      <el-table-column prop="op_type" label="操作类型" width="180"></el-table-column>
      <el-table-column prop="op_details" label="操作详情" width="180"></el-table-column>
      <el-table-column prop="op_times" label="操作时间" width="180"></el-table-column>
      <el-table-column label="再次查看" width="180">
        <template #default="{ row }">
          <el-button type="primary" @click="viewLog(row)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="日志详情" :visible.sync="dialogVisible" width="50%">
      <p>{{ logDetail }}</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  name: "OperationLog",
  data() {
    return {
      // operationLogs: [
      //   {
      //     "ty_name": "超级大台风",
      //     "op_type": 0,
      //     "op_details": "用户‘林狗旺’，新增了台风‘超级大台风’，数据为：lat=74,lon=-26 ,..."
      //   },
      //   {
      //     "ty_name": "超级小台风",
      //     "op_type": 3,
      //     "op_details": "用户‘林狗旺’，对台风‘超级小台风’进行了路径预测，预测结果为：（+3h：lat: 176,lon: -25,usa_wind: 35..."
      //   },
      //   {
      //     "ty_name": "超级小台风",
      //     "op_type": 3,
      //     "op_details": "用户‘林狗旺’，对台风‘超级小台风’进行了路径预测，预测结果为：（+3h：lat: 176,lon: -25,usa_wind: 35..."
      //   },
      //   {
      //     "ty_name": "超级小台风",
      //     "op_type": 3,
      //     "op_details": "用户‘林狗旺’，对台风‘超级小台风’进行了路径预测，预测结果为：（+3h：lat: 176,lon: -25,usa_wind: 35..."
      //   }
      // ],
      operationLogs: [],
      dialogVisible: false,
      logDetail: ""
    };
  },
  created() {
    this.fetchOperationLogs();
  },
  methods: {
    fetchOperationLogs() {
      this.$axios({
        url: 'http://192.168.222.213:8080/logs/search',
        method: 'post',
        data: {
          account_id: this.$cookies.get('account_id')
        }
      })
        .then(response => {
          console.log(response.data)
          if (response.data.success) {
            this.operationLogs = response.data.result;
          } else {
            console.error('获取操作日志失败:', response.data.msg);
          }
        })
        .catch(error => {
          console.error('获取操作日志发生错误:', error);
        });
    },
    //查詢操作記錄(默认直接生成)
    viewLog(log) {
      this.logDetail = log.op_details;
      this.dialogVisible = true;
    },
    //再次查看按钮实现
    clearLogs() {
      this.$axios({
        url: 'http://192.168.222.213:8080/logs/clear',
        method: 'post',
        data: {
          account_id: this.$cookies.get('account_id')
        }
      })
        .then(response => {
          if (response.data.success) {
            this.operationLogs = [];
            this.$message({
              message: '操作日志已成功清空',
              type: 'success'
            });
          } else {
            console.error('清空操作日志失败:', response.data.msg);
          }
        })
        .catch(error => {
          console.error('清空操作日志发生错误:', error);
        });
    //清空日志
    },
    mounted() {
        this.fetchOperationLogs();
        this.clearLogs()
      }
  }
};
</script>

<style scoped>
/* 设置界面背景色 */
.main-content {
  background-color: #ffffff;
}

/* 设置标题颜色 */
h1 {
  color: #409eff;

  .my-table {
    margin-top: 20px;
    /* 上边距为 20px */
    margin-left: 50px;
    /* 左边距为 50px */
  }
}

/* 设置表格的样式 */
.my-table {
  margin-top: 20px;
  /* 上边距为 20px */
  margin-left: 5px;
  /* 左边距为 50px */
  border-collapse: separate;
  /* 使每个单元格之间有空隙 */
  border-spacing: 5 10px;
  /* 设置单元格之间的空隙大小 */
}

/* 设置表格的行样式 */
.my-table .el-table__row {
  background-color: #c541415d;
  /* 设置行的背景颜色 */
  border-radius: 5px;
  /* 设置行的边角半径 */
}

/* 设置按钮的样式 */
.el-button {
  background-color: #409eff;
  /* 设置按钮的背景颜色 */
  border: none;
  /* 去除按钮的边框 */
  box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.1);
  /* 添加按钮的阴影 */
  transition: background-color 0.3s ease;
  /* 添加按钮背景颜色的过渡效果 */
}

.el-button:hover {
  background-color: #2374c1;
  /* 设置按钮鼠标悬停时的背景颜色 */
}</style>


