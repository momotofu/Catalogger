'use strict';

const ENTER_KEY = 13;

// A factory function we can use to create binding handlers for specific
// keycodes.
function keyhandlerBindingFactory(keyCode) {
  return {
    init: function (element, valueAccessor, allBindingsAccessor, data, bindingContext) {
      var wrappedHandler, newValueAccessor;

      // wrap the handler with a check for the enter key
      wrappedHandler = function (data, event) {
        if (event.keyCode === keyCode) {
          valueAccessor().call(this, data, event);
        }
      };

      // create a valueAccessor with the options that we would want to pass to the event binding
      newValueAccessor = function () {
        return {
          keyup: wrappedHandler
        };
      };

      // call the real event binding's init function
      ko.bindingHandlers.event.init(element, newValueAccessor, allBindingsAccessor, data, bindingContext);
    }
  };
}

// a custom binding to handle the enter key
ko.bindingHandlers.enterKey = keyhandlerBindingFactory(ENTER_KEY);

// Category model
class Category {
  constructor(data, isNew) {
    // map data keys and values to Category
    for (let prop in data) {
      if (data.hasOwnProperty(prop))  {
        eval(`this.${prop} = data.${prop}`)
      }
    }

  }
}

// ViewModel
const CategoryList = function(categories) {
  const self = this

  // map array of passed in categories to an observableArray of category objects
  this.categories = ko.observableArray(categories.map((category) => {
    return new Category(category)
  }))

  // state
  this.isEditing = ko.observable(false)
  this.canAdd = ko.observable(false)
  this.activeCategoryId = ko.observable(-1)
  this.isActiveClass = function(id) {
    return this.activeCategoryId() == id ? 'active' : ''
  }.bind(this)

  // setters
  this.setEditing = function() {
    this.isEditing(!this.isEditing())
  }.bind(this)

  this.setCanAdd = function() {
    this.canAdd(!this.canAdd())
  }.bind(this)

  this.setActiveCategoryId = function(id) {
    this.activeCategoryId(id)
  }.bind(this)

  this.createCategory = function() {
  };

  this.deleteCategory = function() {
  }
}



