import * as ko from 'knockout'

// ViewModel
const Items = function() {

  // state
  this.activeCategory = ko.observable(null)
  this.isEditing = ko.observable(false)
  this.activeCategoryName = ko.computed(function() {
    if (this.activeCategory()) {
      return this.activeCategory().name
    } else {
      return 'item'
    }
  }, this)

  /**
   * start - CategoryList delegate methods
   */
  this.setActiveCategory = function(category) {
    this.activeCategory(category)
  }.bind(this)

  this.setIsEditing = function(isEditing) {
    this.isEditing(isEditing)
  }.bind(this)

  /**
   * end - CategoryList delegate methods
   */

}

export default Items
