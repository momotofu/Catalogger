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
      }

      // create a valueAccessor with the options that we would want to pass to the event binding
      newValueAccessor = function () {
        return {
          keyup: wrappedHandler
        }
      }

      // call the real event binding's init function
      ko.bindingHandlers.event.init(element, newValueAccessor, allBindingsAccessor, data, bindingContext)
    }
  }
}

export default keyhandlerBindingFactory
