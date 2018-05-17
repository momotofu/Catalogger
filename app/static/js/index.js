'use strict';

const ENTER_KEY = 13
const ESCAPE_KEY = 27

// A factory function we can use to create binding handlers for specific
// keycodes.
function keyhandlerBindingFactory(keyCode) {
  return {
    init: function (element, valueAccessor, allBindingsAccessor, data, bindingContext) {
      var wrappedHandler, newValueAccessor

      // wrap the handler with a check for the enter key
      wrappedHandler = function (data, event) {
        if (event.keyCode === keyCode) {
          valueAccessor().call(this, data, event)
        }
      };

      // create a valueAccessor with the options that we would want to pass to the event binding
      newValueAccessor = function () {
        return {
          keyup: wrappedHandler
        };
      };

      // call the real event binding's init function
      ko.bindingHandlers.event.init(element, newValueAccessor, allBindingsAccessor, data, bindingContext)
    }
  };
}

// a custom binding to handle the enter key
ko.bindingHandlers.enterKey = keyhandlerBindingFactory(ENTER_KEY);

// another custom binding, this time to handle the escape key
ko.bindingHandlers.escapeKey = keyhandlerBindingFactory(ESCAPE_KEY);


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
      this.id = Math.random().toString(36).substring(7);
      this.name = data.name
      this.depth = -1
      this.type = -1
      this.parentId = -1
    }

  }
}

// TODO: set up api calls

// ViewModel
const CategoryList = function(categories) {
  const self = this

  // state
  this.isEditing = ko.observable(false)
  this.canAdd = ko.observable(false)
  this.activeCategoryId = ko.observable(-1)
  this.isActiveClass = function(id) {
    return this.activeCategoryId() == id ? 'active' : ''
  }.bind(this)


  // setters
  this.setIsEditing = function() {
    this.isEditing(!this.isEditing())

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

    this.setActiveCategoryId(this.categories()[0].id)
  } else {
    this.categories = ko.observableArray([])
  }


  // methods
  this.onAddButtonClick = function() {
    this.setCanAdd()

    const el = document.getElementById('canAddInput')

    if (this.canAdd()) {
      el.focus()
    } else {
      el.value = ""
    }

  }.bind(this)

  this.createCategory = function(context, event) {
    const el = event.target
    const name = el.value

    if (name.length > 0) {
      // create a new dummy category and get a reference to its id
      const category = new Category({ name }, true)

      // update the DOM
      this.categories.unshift(category)
      console.log('categories before: ', this.categories())

      // clear and hide input element
      el.value = ""
      this.canAdd(false)

      // update server
      $.post({
        url : '/categories/new',
        data : {
          name
        },
        success: handleSuccess.bind(this),
        dataType: 'json'
      })

      // success handler for AJAX POST request
      function handleSuccess(data) {
        // success message
        console.log(`Successfuly created "${data.name}" category on the server.`)

        // update the dummy category object with real data
        for (let key in data) category[key] = data[key]
      }

    }
  }

  this.deleteCategory = function(id, context, event) {
    // handle event object
    this.inputClicked(context, event)

    // delete category object from DOM
    this.categories.remove(context)

    // remove category from server
    $.post({
      url : `/categories/${id}/delete`,
      data : {
        name
      },
      success: function(data) {
        // success message
        console.log(`Successfuly deleted ${data.name}" category on the server.`)
      },
      dataType: 'json'
    })

  }.bind(this)

  this.inputClicked = function(context, event) {
    event.preventDefault()
    event.stopPropagation()
  }

}



