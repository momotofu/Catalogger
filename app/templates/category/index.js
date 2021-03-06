import * as ko from 'knockout'
import { keyhandlerBindingFactory } from '../utils/js/utils'

const ENTER_KEY = 13
const ESCAPE_KEY = 27

// a custom binding to handle the enter key
ko.bindingHandlers.enterKey = keyhandlerBindingFactory(ENTER_KEY)

// another custom binding, this time to handle the escape key
ko.bindingHandlers.escapeKey = keyhandlerBindingFactory(ESCAPE_KEY)


// Category model
class Category {
  constructor(data, isPlaceholder) {
    // keep track of whether or not Category is a dummy,
    // and need's to be updated from the server
    this.isPlaceholder = isPlaceholder

    if (!isPlaceholder) {
      // map data keys and values to Category
      for (let prop in data) {
        if (data.hasOwnProperty(prop))  {
          eval(`this.${prop} = data.${prop}`)
        }
      }

    } else {
      // give object filler attribute values to satisify the DOM
      this.id = Math.random().toString(36).substring(7)
      this.name = data.name
      this.depth = -1
      this.type = -1
      this.parentId = -1
    }

  }
}

// ViewModel
const CategoryList = function(categories, delegate, category_id) {
  this.delegate = delegate
  this.confirmDeleteModal = $('#confirmDeleteModal')


  // state
  this.isEditing = ko.observable(false)
  this.canAdd = ko.observable(false)
  this.activeCategoryId = ko.observable(-1)
  this.isActiveClass = function(id) {
    return this.activeCategoryId() == id ? 'active' : ''
  }.bind(this)
  this.editedCategories = []


  // getters
  this.getCategory = function(id) {
    return this.categories().filter((category) => {
      return category.id === id
    })[0]
  }


  // setters
  this.setIsEditing = function() {
    this.isEditing(!this.isEditing())
    this.delegate.setIsEditing(this.isEditing())

    if (this.isEditing() && this.canAdd()) {
      this.setCanAdd()
    }

  }.bind(this)

  this.setCanAdd = function() {
    this.canAdd(!this.canAdd())

    if (this.isEditing() && this.canAdd) {
      this.setIsEditing()
    }

  }.bind(this)

  this.setActiveCategoryId = function(id) {
    this.activeCategoryId(id)

  }.bind(this)


  // map array of passed in categories to an observableArray of category objects
  if (categories.length > 0) { // protect against null list
    this.categories = ko.observableArray(categories.map((category) => {
      return new Category(category)
    }))
  } else {
    this.categories = ko.observableArray([])
  }

  // this state is down here because its dependent on this.categories
  this.canEdit = ko.computed(() => {
    const canEdit = this.categories().length > 0
    if (!canEdit && this.isEditing()) {
      this.setIsEditing()
    }

    return !canEdit
  }, this)


  // methods
  this.categoryEditedEnterKeyHandler = function(context, event) {
    this.categoryEdited(context, event)
    this.onEditButtonClick()

  }.bind(this)

  this.categoryEdited = function(context, event) {
    // update DOM
    if (event.target.value.length > 0 && event.target.placeholder != event.target.value) {
      context.name = event.target.value

      // add category object to editedCategories list
      this.editedCategories.push(context)
    }

  }.bind(this)

  this.onEditButtonClick = function() {
    this.setIsEditing()

    if (!this.isEditing()) {
      // update server
      $.post({
        url : '/categories/update',
        data : {
          categories : JSON.stringify(this.editedCategories)
        },
        success: successHandler.bind(this),
        dataType: 'json'
      })

      function successHandler(data) {
        // success message
        console.log('Successfuly updated categories on the server.')

        // reset editedCategories
        this.editedCategories = []
      }
    }

    this.setFirstCategoryBorderRadius()

  }.bind(this)

  this.onAddButtonClick = function() {
    this.setCanAdd()

    const el = document.getElementById('canAddInput')

    if (this.canAdd()) {
      el.focus()
    } else {
      el.value = ""
    }

    this.setFirstCategoryBorderRadius()

  }.bind(this)

  this.setFirstCategoryBorderRadius = function() {
    // change first list item border-radius
    const firstCategory = document.getElementById('category-list').children[1]

    if (firstCategory) {
      if (!this.canAdd()) {
        firstCategory.style.borderTopRightRadius = '3px'
        firstCategory.style.borderTopLeftRadius = '3px'
      } else {
        firstCategory.style.borderTopRightRadius = '0px'
        firstCategory.style.borderTopLeftRadius = '0px'
      }
    }

  }.bind(this)

  this.createCategory = function(context, event) {
    const el = event.target
    const name = el.value

    if (name.length > 0) {
      // create a new dummy category and get a reference to its id
      const category = new Category({ name }, true)
      this.setActiveCategoryId(category.id)

      // update the DOM
      this.categories.unshift(category)

      // clear and hide input element
      el.value = ""
      this.canAdd(false)

      // update server
      $.post({
        url : '/categories/new',
        data : {
          name
        },
        success: successHandler.bind(this),
        dataType: 'json'
      })

      // success handler for AJAX POST request
      function successHandler(data) {
        // success message
        console.log(`Successfuly created "${data.name}" category on the server.`)

        // update the dummy category object with real data
        for (let key in data) category[key] = data[key]
        this.setActiveCategoryId(data['id'])

        this.setFirstCategoryBorderRadius()
      }

    }
  }

  this.toggleModal = function() {
    this.confirmDeleteModal.modal('toggle')

  }.bind(this)

  this.deleteCategory = function(event) {
    const id = this.activeCategoryId()
    const category = this.getCategory(id)

    // delete category object from DOM
    this.setActiveCategoryId(-1)
    this.categories.remove(category)
    this.confirmDeleteModal.modal('hide')

    // remove category from server
    $.post({
      url : `/categories/${id}/delete`,
      data : {
        name
      },
      success: function(data) {
        // success message
        console.log(`Successfuly deleted "${data.name}" category on the server.`)
      },
      dataType: 'json'
    })

    this.setFirstCategoryBorderRadius()

  }.bind(this)

  this.inputClicked = function(context, event) {
    event.preventDefault()
    event.stopPropagation()
  }

  // setup subscriptions
  this.activeCategoryId.subscribe(function(newValue) {
    const category = this.getCategory(newValue)
    this.delegate.setActiveCategory(category)
  }, this)

  // setup categoryList
  this.init = function() {
    if (category_id !== 'None') {
      // ensure id is an integer
      if (typeof(category_id) === 'string') category_id = parseInt(category_id)

      this.setActiveCategoryId(category_id)

    } else if (this.categories().length > 0) {
      // if there are categories then set active id to the first category
      this.setActiveCategoryId(this.categories()[0].id)
    }
  }
}

export default CategoryList
