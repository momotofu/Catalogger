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
  this.activeItem = {}
  this.isEditing = ko.observable(false)
  this.items = ko.observableArray()
  this.canCreateItem = ko.computed(() => {
    console.log('canCreateItem: ', this.activeCategory())
    return !this.activeCategory()
  })
  this.activeCategoryName = ko.computed(function() {
    if (this.activeCategory()) {
      return this.activeCategory().name
    } else {
      return 'Item'
    }
  }, this)

  // constants
  this.confirmDeleteModal = $('#confirmItemDeleteModal')


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


  // getters
  this.getItemsForActiveCategory = function() {
    // reset items collection if no category is selected
    if (!this.activeCategory()) {
      this.items([])
      return
    }

    // setup get URL
    const id = this.activeCategory().id
    const baseURL = getBaseURLFrom(window.location.href)
    const url = `${baseURL}/category/${id}/items`

    // get item JSON
    $.get({
      url,
      success: handleSuccess.bind(this)
    })

    function handleSuccess(data) {
      console.log('successfuly retreived item data')
      const dataJSON = JSON.parse(data)

      // update displayed items
      this.items(dataJSON.map((itemData) => {
        return new Item(itemData)
      }))
    }

  }

  this.getItemImageURL = function(imageName) {
    // setup URL
    const baseURL = getBaseURLFrom(window.location.href)
    const url = `${baseURL}/images/${imageName}`

    return `url(${url})`
  }


  // methods
  this.sendToCreateItem = function(context, event) {
    event.preventDefault()
    event.stopPropagation()

    const id = this.activeCategory().id
    const baseURL = getBaseURLFrom(window.location.href)

    window.location.href = `${baseURL}/category/${id}/items/new`
  }.bind(this)

  this.sendToEditItem = function(context, event) {
    event.preventDefault()
    event.stopPropagation()

    const categoryId = context.categories_ids[0]
    const id = context.id
    const baseURL = getBaseURLFrom(window.location.href)

    window.location.href = `${baseURL}/category/${categoryId}/items/${id}/edit`
  }

  this.deleteItem = function() {
    // delete item object from DOM
    const item = this.activeItem
    this.items.remove(item)
    this.confirmDeleteModal.modal('hide')

    // set up url
    const categoryId = item.categories_ids[0]
    const id = item.id
    const baseURL = getBaseURLFrom(window.location.href)
    const url =`${baseURL}/category/${categoryId}/items/${id}/delete`

    // remove category from server. This removes the item from the category. If
    // the item has no more categories, then it will be deleted.
    $.post({
      url : url,
      success: function(data) {
        const json = JSON.parse(data)
        // success message
        console.log(`Successfuly deleted "${json.name}" item on the server.`)
      }
    })

  }.bind(this)

  this.toggleModal = function(context, event) {
    event.preventDefault()
    event.stopPropagation()

    // set active item to be referenced by the deleteItem function
    this.activeItem = context
    this.confirmDeleteModal.modal('toggle')

  }.bind(this)

}

export default Page
