import * as ko from 'knockout'
import { getBaseURLFrom } from '../utils/js/utils'

// Item model
class Item {
  constructor(data) {
    // map data keys and values to Category
    for (let prop in data) {
      if (data.hasOwnProperty(prop))  {
        eval(`this.${prop} = data.${prop}`)
      }
    }
  }
}

// ViewModel
const Page = function() {

  // state
  this.activeCategory = ko.observable(null)
  this.isEditing = ko.observable(false)
  this.items = ko.observableArray()
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
    this.getItemsForActiveCategory()
  }.bind(this)

  this.setIsEditing = function(isEditing) {
    this.isEditing(isEditing)
  }.bind(this)
  /**
   * end - CategoryList delegate methods
   */


  // methods
  this.sendToCreateItem = function(context, event) {
    event.preventDefault()
    event.stopPropagation()

    const id = this.activeCategory().id
    const baseURL = getBaseURLFrom(window.location.href)

    window.location.href = `${baseURL}/category/${id}/items/new`
  }.bind(this)

  this.getItemsForActiveCategory = function() {
    // get item JSON
    const id = this.activeCategory().id
    const baseURL = getBaseURLFrom(window.location.href)
    const url = `${baseURL}/category/${id}/items`

    $.get(url, function(data) {
      console.log('success with data: ', data)
    })

  }

}

export default Page
