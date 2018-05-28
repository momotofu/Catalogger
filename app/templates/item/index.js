const CreateItemViewModel = function() {
  // constants
  this.imageInput = $('#image-input')
  this.imagePreview = $('#image-upload-preview')

  // methods
  this.displayImage = function(event) {
    const input = this.imageInput[0]

    // check if input has a file
    if (input.files && input.files[0]) {
      const reader = new FileReader();

      reader.onload = function(event) {
        // set the image preview element src to the uploaded file
        this.imagePreview
          .css('background-image', `url(${event.target.result})`)
          .css('background-position', 'center')
          .css('background-repeat', 'no-repeate')
          .css('background-size', 'cover')
      }.bind(this)

      reader.readAsDataURL(input.files[0])
    }

  }.bind(this)

  this.openFileChooser = function(event) {
    this.imageInput.click()
  }.bind(this)

}

export default CreateItemViewModel
