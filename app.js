
function setCookie(cname, cvalue, exdays) {
var d = new Date();
d.setTime(d.getTime() + (exdays*24*60*60*1000));
var expires = "expires="+ d.toUTCString();
document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
var name = cname + "=";
var decodedCookie = decodeURIComponent(document.cookie);
var ca = decodedCookie.split(';');
for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
        c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
    }
}
return "";
}

let loc = getCookie('last-loc');

Vue.component('Riddle', {
  props: {
    index: Number,
    riddle: Object,

    // Dynamic
    filter: String,
    search_location: String,
    show: Boolean,
  },
  watch: {
    filter: function() {
      this.applyFilter();
    },
    search_location: function() {
      this.applyFilter();
    }
  },
  methods: {
    applyFilter: function() {
      let show = true;
      if(this.search_location.length==1) {
        show = this.filter.length >= 1;
      } else if(this.search_location.length==2) {
        show = (this.riddle.Location == this.search_location);
      }
      if (show && this.filter.length>0) {

        if(this.filter.length>3) {
          if(this.riddle.Index[this.filter.slice(0, 3)]) {
            show = (this.riddle.Search.indexOf(this.filter) >= 0);
          } else {
            show = false;
          }
        } else {
          show = this.riddle.Index[this.filter];
        }

      }
      this.show = show
    }
  },
  //
  template: `
    <div
      v-if="riddle.Answer=='?'"
      v-show="show" class='result' :class="[show ? 'shown': '']">
      <span class='location' v-show="search_location.length<2">{{riddle.Location}}</span>
      <div class='riddle' v-html="riddle.Riddle"></div>
      <span class='answer'>
        ({{riddle.Hint}})
      </span>
      <div class="wrong"><a target="_blank" :href="riddle['Prefilled URL']">Submit answer</a></div>
    </div>
    <div
      v-else
      v-show="show" class='result' :class="[riddle.Answer, show ? 'shown': '']">
      <span class='location' v-show="search_location.length<2">{{riddle.Location}}</span>
      <div class='riddle' v-html="riddle.Riddle"></div>
      <span class='answer'>
        <img :src="'img/stat_'+riddle.Answer+'.png'" :class='{has_hint:riddle.Hint}'/>
        <div v-if="riddle.Hint" class="hint">{{riddle.Hint}}</div>

      </span>
      <div class="wrong"><a target="_blank" :href="riddle['Prefilled URL']">nope</a></div>
    </div>
    `,
})

let answer_images = {
  "Yellow / Tenacity": "tnc",
  "Red / Honor": "hnr",
  "Green / Charm": "crm",
  "Blue / Comprehension": "cmp",
}
let location_map = {
  "Louise Hill": "LH",
  "3's Forest": "3F",
  "Silvie's Mine": "SM",
  "Aviar Cove": "AV",
  "Vaer Reef": "VR",
}
var app = new Vue({
  el: '#app',
  data: {
    filter: '',
    search_location: loc,
    riddles: [],
    mark: Object,
  },
  computed: {
    fiterLower: function() {
      return this.filter.toLowerCase()
    }
  },
  methods: {
    focusSearch: function() {
      this.$refs.filter.focus();
      this.$refs.filter.select();
    },
    saveLocation: function() {
      setCookie('last-loc', this.search_location, 30)
    }
  },
  created: function() {
    let $this = this;
    Papa.parse("values.csv?v=0004", {
      download: true,
      header: true,
      step: function(row) {
        //row.data.Riddle = row.data.Riddle.replaceAll("\n","<br>")
        if(!row.data.Riddle) return;
        if(row.data.Answer != "?") {
          row.data.Answer = answer_images[row.data.Answer];
        }
        row.data.Search = row.data.Riddle.replaceAll(/(<([^>]+)>)/ig,'').toLowerCase();

        row.data.Index = JSON.parse(row.data.Index);
        row.data.Location = location_map[row.data.Location];
        $this.riddles.push(row.data)
      },
      complete: function() {
      }
    });
  },
  mounted: function () {
    let $this = this;
    this.$nextTick(function () {
      $this.mark = new Mark($this.$el);
    })
  },

  updated: function () {
    let $this = this;
    this.$nextTick(function () {
      $this.mark.unmark({
        done:function(){
          if($this.filter.length>3){
            var context = document.querySelectorAll(".shown");
            var instance = new Mark(context);
            instance.mark($this.filter, {
              separateWordSearch: false,
            })
          }
        }
      })
    })
  },
})
Vue.component('riddle')

window.addEventListener("keydown",function (e) {
    if (e.keyCode === 114 || (e.ctrlKey && e.keyCode === 70)) {
      app.focusSearch();
        e.preventDefault();
    }
})
