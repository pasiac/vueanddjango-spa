<template>
  <div class="home">
    <h1 class="title">Django i vue</h1>

    <hr>

    <div class="columns">
      <div class="column is-5 is-offset-5">
        <form v-on:submit.prevent="addTask">
          <h2 class="subtitle">Dodaj zadanie</h2>

          <div class="field">
            <label class="label">Opis</label>
            <div class="control">
              <input class="input" type="text" v-model="description">
            </div>
          </div>

          <div class="field">
            <label class="label">Status</label>
            <div class="control">
              <div class="select">
                <select v-model="status">
                  <option value="todo">To do</option>
                  <option value="done">Zrobione</option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Spedzony czas (minuty)</label>
            <div class="control">
              <input class="input" type="number" v-model="minutes_spend">
            </div>
          </div>

          <div class="field">
            <label class="label">Czy było fajne</label>
            <div class="control">
              <input class="checkbox" type="checkbox" v-model="enjoyed">
            </div>
          </div>

          <div class="field">
            <label class="label">Osoba </label>
            <div class="control">
              <input class="input" type="text" v-model="person">
            </div>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-link">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <div class="columns">
      <div class="column is-6">
        <h2 class="subtitle">To do</h2>

        <div class="todo">
          <div class="card" v-for="task in tasks" v-if="task.status === 'todo'" v-bind:key="task.id">
            <div v-if="editTagId == task.id">
              <label>Description</label><br>
              <input
                v-if="editTagId"
                v-model="task.description"
              ><br>
              <label>Enjoyed</label><br>

              <input type="checkbox"
                v-if="editTagId"
                v-model="task.enjoyed"
              ><br>
              <label>Time spend</label><br>
              <input type="number"
                v-if="editTagId"
                v-model="task.minutes_spend"
              ><br>
              <label>Person</label><br>
             <input
                v-if="editTagId"
                v-model="task.person"
              ><br>
              <a class="card-footer-item" @click="editTask(task.id);">Edit</a>
            </div>
            <div @click="editTagId=task.id" v-else>
              <p class="card-content">{{ task.description }}</p>
              <p class="card-content">enjoyed: {{ task.enjoyed }}</p>
              <p class="card-content">time spend: {{ task.minutes_spend}}</p>
              <p class="card-content" v-if="task.person">person: {{ task.person}}</p>
            </div>
            <footer class="card-footer">
              <a class="card-footer-item" @click="setStatus(task.id, 'done')">Done</a>
              <a class="card-footer-item" @click="deleteTask(task.id)">Delete</a>
            </footer>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <h2 class="subtitle">Zrobione</h2>

        <div class="done">
          <div class="card" v-for="task in tasks" v-if="task.status === 'done'" v-bind:key="task.id">
            <div>
              <p class="card-content">{{ task.description }}</p>
              <p class="card-content">enjoyed: {{ task.enjoyed }}</p>
              <p class="card-content">time spend: {{ task.minutes_spend}}</p>
              <p class="card-content">person: {{ task.person}}</p>
            </div>
            <footer class="card-footer">
              <a class="card-footer-item" @click="setStatus(task.id, 'todo')">To do</a>
              <a class="card-footer-item" @click="deleteTask(task.id)">Delete</a>

            </footer>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_URL = 'http://127.0.0.1:8000/'

import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      tasks: [],
      description: '',
      status: 'todo',
      enjoyed: '',
      minutes_spend: 0,
      person: '',
      editTagId: ''
    }
  },
  mounted () {
    this.getTasks()
  },
  methods: {
    getTasks() {
      axios({
        method: 'get',
        url: API_URL + 'tasks/',
        auth: {
          username: 'admin',
          password: 'admin'
        }
      }).then(response => this.tasks = response.data)
    },
    deleteTask(task_id) {
        axios({
          method: 'delete',
          url: API_URL + 'tasks/' + task_id + '/',
          data: {
            description: this.description,
            status: this.status,
            enjoyed: this.enjoyed,
            minutes_spend: this.minutes_spend,
            person: this.person
          },
          auth: {
            username: 'admin',
            password: 'admin'
          }
        }).then((response) => {
          const task_index = this.tasks.findIndex(p => p.id === task_id)
          this.tasks.splice(task_index, 1)
        }).catch((error) => {
          console.log(error)
        })
    },
    addTask() {
      if (this.description) {
        axios({
          method: 'post',
          url: API_URL + 'tasks/',
          data: {
            description: this.description,
            status: this.status,
            enjoyed: this.enjoyed,
            minutes_spend: this.minutes_spend,
            person: this.person
          },
          auth: {
            username: 'admin',
            password: 'admin'
          }
        }).then((response) => {
          let newTask = {
            'id': response.data.id,
            'description': this.description,
            'status': this.status,
            'enjoyed': this.enjoyed,
            'minutes_spend': this.minutes_spend,
            'person': this.person
          }

          this.tasks.push(newTask)

          this.description = ''
          this.status = 'todo'
          this.enjoyed = ''
          this.minutes_spend = 0
          this.person = ''
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    editTask(task_id) {
      const task = this.tasks.filter(task => task.id === task_id)[0]
      const description = task.description
      const enjoyed = task.enjoyed
      const minutes_spend = task.minutes_spend
      const person = task.person
      const status = task.status

      axios({
        method: 'put',
        url: API_URL + 'tasks/' + task_id + '/',
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          status: status,
          description: description,
          enjoyed: enjoyed,
          minutes_spend: minutes_spend,
          person: person
        },
        auth: {
          username: 'admin',
          password: 'admin'
        }

      }).then(() => {
        task.description = description
        task.status = status
        task.enjoyed = enjoyed
        task.minutes_spend = minutes_spend
        task.person = person
        this.editTagId = ''
      })
    },
    setStatus(task_id, status) {
      const task = this.tasks.filter(task => task.id === task_id)[0]
      const description = task.description
      const enjoyed = task.enjoyed
      const minutes_spend = task.minutes_spend
      const person = task.person

      axios({
        method: 'put',
        url: API_URL + 'tasks/' + task_id + '/',
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          status: status,
          description: description,
          enjoyed: enjoyed,
          minutes_spend: minutes_spend,
          person: person
        },
        auth: {
          username: 'admin',
          password: 'admin'
        }
      }).then(() => {
        task.status = status
      })
    }
  }
}
</script>

<style lang="scss">
.select, select {
  width: 100%;
}

.card {
  margin-bottom: 20px;
}

.done {
  opacity: 0.3;
}
</style>
