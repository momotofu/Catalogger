import * as ko from 'knockout'

// ViewModel
const Items = function() {

  // CategoryList methods
  this.activeCategoryId = -1
  this.setActiveCategoryId = function(id) {
    this.activeCategoryId = id
  }.bind(this)
}

export default Items
