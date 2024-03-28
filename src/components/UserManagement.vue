<!-- 这个模板中，我使用了一个简单的 HTML 表格来显示用户信息，并添加了删除和编辑按钮。
  编辑按钮会打开一个模态窗口，用于输入新的用户名。用户提交表单后，editUser 方法会被调用，
  并将新的用户名发送到服务器。如果成功，模态窗口将关闭，并重新获取用户列表 -->
  <template>
    <div class="user-container">
      <el-table :data="userData" stripe border>
        <el-table-column prop="id_dist" label="账号 ID"></el-table-column>
        <el-table-column prop="user_name" label="用户名"></el-table-column>
        <el-table-column label="管理员">
          <template slot-scope="scope">
            {{ scope.row.isAdmin ? '是' : '否' }}
          </template>
        </el-table-column>
  
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="small" type="danger" @click="deleteUser(scope.row.id_dist)">删除</el-button>
            <el-button size="small" type="success" @click="openEditModal(scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 编辑用户信息的模态框 -->
      <el-dialog title="编辑用户信息" :visible.sync="isEditModalOpen" width="50%" append-to-body>
        <el-form :model="editingData" status-icon :rules="editrules" ref="editingData">
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="editingData.new_user_name" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="closeEditModal">取 消</el-button>
          <el-button type="primary" @click="editUser(editingData.account_id, editingData.new_user_name)">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </template>
    
  <script>
  export default {
    data() {
      return {
        //     userData: [
        //   {
        //     id_dist: "111111",
        //     user_name: "WangYijia",
        //     isAdmin: true,
        //   },
        //   {
        //     id_dist: "123456",
        //     user_name: "陈昱鑫",
        //     isAdmin: true,
        //   },
        //   {
        //     id_dist: "178978",
        //     user_name: "王二嘉",
        //     isAdmin: false,
        //   },
        // ],
        userData: [],
        isEditModalOpen: false,
        editingData: { account_id: '', new_user_name: '' },
        editrules: {
          new_user_name: [
            { required: true, message: "用户名不能为空！", trigger: "blur" },
          ]
        },
      };
    },
    methods: {
  
      getUsers() {
        this.$axios({
          url: 'http://192.168.222.213:8080/users/user_list',
          method: 'post',
          data: {
            account_id: this.$cookies.get('account_id')
          }
        })
          .then(response => {
            console.log(response.data.msg);
            if (response.data.success) {
              this.userData = response.data.result;
            } else {
              
              if (response.status == 401 || response.status == 403) {
                this.$router.push('/home');
              }
            }
          }
          );
      },
  
      deleteUser(account_id, id_dist) {
    this.$axios({
      url: 'http://192.168.222.213:8080/users/delete',
      method: 'post',
      data: {
        account_id: account_id,
        id_dist: id_dist
      },
    })
      .then(response => {
        if (response.data.success) {
          this.getUsers();
        } else {
          console.log(response.data.msg);
          if (response.status == 401 || response.status == 403) {
            this.$router.push('/home');
          }
        }
      });
  },
  
  editUser(account_id, id_dist,new_user_name) {
    this.$axios({
      url: 'http://192.168.222.213:8080/users/alter',
      method: 'post',
      data: {
        account_id: account_id,
        id_dist: id_dist,
        new_user_name: new_user_name
      },
    })
      .then(response => {
        if (response.data.success) {
          this.isEditModalOpen = false;
          this.getUsers();
        } else {
          console.log(response.data.msg);
          if (response.status == 401 || response.status == 403) {
            this.$router.push('/home');
          }
        }
      });
  },
  
      openEditModal(user) {
        this.isEditModalOpen = true;
        this.editingData = { id_dist: user.id_dist, new_user_name: '' };
      },
    },
    mounted() {
      // let userInfo = JSON.parse(this.getCookie('user_info'));
      // if (!userInfo || !userInfo.isAdmin) {
      //   alert('只有管理员用户才能访问此页面');
      //   this.$router.push('/home');
      //   return;
      // }
      this.getUsers();
    }
  }
  </script>