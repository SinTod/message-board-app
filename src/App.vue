<!--suppress ALL -->
<template>
  <div id="app">
    <div class="container">
      <h1 class="title">Message Board</h1>
        <form action="/api/messages" method="POST" @submit.prevent="addMessage" @keydown="errors.clear($event.target.name)">
          <div :class="['form-group', {'has-error': errors.has('name')}]">
            <input type="text" class="form-control" name="name" placeholder="Name" v-model="name">
            <span class="help-block" v-if="errors.has('name')" v-text="errors.get('name')"></span>
          </div>
          <div :class="['form-group', {'has-error': errors.has('text')}]">
            <textarea class="form-control" name="text" rows="5" placeholder="Say something..." v-model="text"></textarea>
            <span class="help-block" v-text="errors.get('text')"></span>
          </div>
          <button class="btn btn-default" :disabled="errors.any()">Submit</button>
        </form>
        <div class="messages-header">{{ messages.length }} messages</div>
        <div class="messages">
          <ul tansition="fade">
            <template v-for="message in messages">
              <message-item :message="message"></message-item>
            </template>
          </ul>
        </div>
    </div>
  </div>
</template>

<script>
import MessageItem from './components/MessageItem.vue'
var axios = require('axios')

// 将 errors 相关操作封装成为一个类，使代码开起来更清晰
class Errors {
  constructor() {
    this.errors = { }
  }

  // 某个输入框数据是否有错误
  has(field) {
    return this.errors.hasOwnProperty(field)
  }

  // 任何一个输入框数据有错误返回true
  any() {
    return Object.keys(this.errors).length > 0
  }

  // 获取输入框的第一个错误（每个输入框的错误是个列表）
  get(field) {
    if (this.errors[field]) {
      return this.errors[field][0]
    }
  }

  // 初始化 errors
  record(errors) {
    this.errors = errors
  }

  // 清除某个输入框的错误
  clear(field) {
    delete this.errors[field]
  }
}

export default {
  name: 'app',
  data () {
    return {
      name: '',
      text: '',
      messages: [],
      errors: new Errors()
    }
  },
  methods: {
    // 点击 Submit 会触发此事件，向服务器发送 POST 请求
    addMessage() {
      axios.post('/api/messages', {
        'name': this.name,
        'text': this.text
      }).then(response => {
        if (response.data.ok) {
          this.messages.unshift({
            'name': this.name,
            'text': this.text,
            'created_at': new Date().toISOString()
          })
          this.name = ''
          this.text = ''
        }
      // 当返回错误时，初始化 errors
      }).catch(error => this.errors.record(error.response.data.errors))
    }
  },
  mounted() {
    axios.get('/api/messages').then(response => this.messages = response.data)
  },
  components: {
    MessageItem
  }
}
</script>

<style>
    .container {
        width: 650px;
        margin-top: 60px;
    }

    #app {
        margin: 0 auto;
    }

    .title {
        text-align: center;
        margin-bottom: 20px;
        color: #e3e3e3;
    }

    .messages-header {
        line-height: 1;
        color: #666;
        padding: 20px 0 6px;
        border-bottom: 1px solid #eee;
        text-transform: uppercase;
        font-size: 13px;
    }

    .messages ul {
        margin: 0;
        padding: 0;
    }
</style>