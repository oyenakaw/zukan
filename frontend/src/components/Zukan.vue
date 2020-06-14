<template>
  <div id="app">
    <div><input type="file" @change="selectedFile"></div>
    <div><img v-show="uploadedImage" :src="uploadedImage" /></div>
    <div><button class="btn btn-info" type="button" @click="predict">Upload</button></div>
    <!-- <div><img :src="image"></div> -->
    <div>{{ label }}</div>
    <ul>
      <li v-for="(w, key) in wiki" :key="key">
        <span>{{ w.extract}}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  el: '#app',
  data () {
    return {
      file: null,
      uploadedImage: null,
      image: null,
      label: null,
      wiki: null
    }
  },
  // TODO
  filters: {
    paragraph: function (str) {
      // return str.replace(/== (.?) ==/g, '===')
      const p = /(.+?) == |(.+?)$/g
      const pList = str.match(p)
      return pList
    }
  },
  methods: {
    selectedFile (e) {
      this.image = null
      this.label = null
      this.wiki = null
      this.file = e.target.files[0]
      this.createImage(this.file)
    },
    async predict () {
      const form = new FormData()
      form.append('img_file', this.file)
      await axios
        .post('/api/predict', form, {
          headers: {
            'content-type': 'multipart/form-data'
          }
        })
        .then(response => {
          // const prefix = 'data:image/jpg;base64,'
          // this.image = prefix + response.data.image
          this.label = response.data.label
        })
        .catch(error => {
          console.log(error)
        })
      await axios
        .get('https://ja.wikipedia.org/w/api.php', {
          params: {
            action: 'query',
            format: 'json',
            prop: 'extracts',
            exintro: '',
            explaintext: '',
            titles: this.label,
            origin: '*'
          },
          responseType: 'json',
          'headers': {
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          this.wiki = response.data.query.pages
        })
        .catch(error => console.log(error))
    },
    createImage (file) {
      let reader = new FileReader()
      reader.onload = (e) => {
        this.uploadedImage = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
}
</script>
