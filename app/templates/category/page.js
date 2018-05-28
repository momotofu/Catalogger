import * as ko from 'knockout'
import { getBaseURLFrom } from '../utils/js/utils'

// ViewModel
const Page = function() {

  // state
  this.activeCategory = ko.observable(null)
  this.isEditing = ko.observable(false)
  this.activeCategoryName = ko.computed(function() {
    if (this.activeCategory()) {
      return this.activeCategory().name
    } else {
      return 'Item'
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


  // methods
  this.sendToCreateItem = function(context, event) {
    console.log(context, event)
    event.preventDefault()
    event.stopPropagation()

    const id = this.activeCategory().id
    const baseURL = getBaseURLFrom(window.location.href)

    window.location.href = `${baseURL}/category/${id}/items/new`
  }.bind(this)

}

export default Page
