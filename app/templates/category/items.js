import * as ko from 'knockout'

// ViewModel
const Items = function() {

  // state
  this.activeCategory = null

  // CategoryList delegate method
  this.setActiveCategory = function(category) {
    this.activeCategory = category
    console.log('category: ', category)
  }.bind(this)


  // methods

}

export default Items
